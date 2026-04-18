#define _POSIX_C_SOURCE 200809L

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#pragma pack(push, 1)
typedef struct {
    uint32_t seq;
    uint64_t send_ts_ns;
} PacketHeader;
#pragma pack(pop)

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

static void sleep_us(int us) {
    if (us <= 0) {
        return;
    }
    struct timespec req;
    req.tv_sec = us / 1000000;
    req.tv_nsec = (long)(us % 1000000) * 1000L;
    nanosleep(&req, NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 7) {
        fprintf(stderr,
                "Usage: %s <server_ip> <port> <duration_sec> <packet_size_bytes> <interval_us> <output_prefix>\n",
                argv[0]);
        return 1;
    }

    const char *server_ip = argv[1];
    int port = atoi(argv[2]);
    int duration_sec = atoi(argv[3]);
    int packet_size = atoi(argv[4]);
    int interval_us = atoi(argv[5]);
    const char *prefix = argv[6];

    if (port <= 0 || port > 65535 || duration_sec <= 0 || packet_size < (int)sizeof(PacketHeader) || packet_size > 65507 || interval_us < 0) {
        fprintf(stderr, "Invalid arguments\n");
        return 1;
    }

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket");
        return 1;
    }

    struct timeval timeout;
    timeout.tv_sec = 0;
    timeout.tv_usec = 300000;
    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) < 0) {
        perror("setsockopt");
        close(sockfd);
        return 1;
    }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons((uint16_t)port);
    if (inet_pton(AF_INET, server_ip, &server_addr.sin_addr) <= 0) {
        fprintf(stderr, "Invalid server IP\n");
        close(sockfd);
        return 1;
    }

    unsigned char *send_buf = (unsigned char *)malloc((size_t)packet_size);
    unsigned char *recv_buf = (unsigned char *)malloc((size_t)packet_size);
    if (send_buf == NULL || recv_buf == NULL) {
        fprintf(stderr, "Failed to allocate buffers\n");
        free(send_buf);
        free(recv_buf);
        close(sockfd);
        return 1;
    }

    char throughput_path[512];
    char delay_path[512];
    snprintf(throughput_path, sizeof(throughput_path), "%s_throughput.csv", prefix);
    snprintf(delay_path, sizeof(delay_path), "%s_delay.csv", prefix);

    FILE *f_thr = fopen(throughput_path, "w");
    FILE *f_dly = fopen(delay_path, "w");
    if (f_thr == NULL || f_dly == NULL) {
        fprintf(stderr, "Failed to open CSV output files\n");
        free(send_buf);
        free(recv_buf);
        close(sockfd);
        if (f_thr != NULL) fclose(f_thr);
        if (f_dly != NULL) fclose(f_dly);
        return 1;
    }

    fprintf(f_thr, "second,throughput_mbps\n");
    fprintf(f_dly, "second,avg_delay_ms\n");

    uint64_t start_ns = now_ns();
    uint64_t end_ns = start_ns + (uint64_t)duration_sec * 1000000000ULL;
    uint64_t next_window_ns = start_ns + 1000000000ULL;

    uint64_t bytes_received_window = 0;
    double delay_sum_ms_window = 0.0;
    int delay_samples_window = 0;
    int second_idx = 1;

    uint64_t total_bytes_received = 0;
    double total_delay_ms = 0.0;
    int total_received = 0;
    int total_sent = 0;

    while (now_ns() < end_ns) {
        memset(send_buf, 'A' + (total_sent % 26), (size_t)packet_size);
        PacketHeader *h = (PacketHeader *)send_buf;
        h->seq = htonl((uint32_t)total_sent);

        uint64_t send_time = now_ns();
        h->send_ts_ns = send_time;

        ssize_t sent = sendto(sockfd, send_buf, (size_t)packet_size, 0,
                              (struct sockaddr *)&server_addr, sizeof(server_addr));
        if (sent < 0) {
            perror("sendto");
            break;
        }
        total_sent++;

        struct sockaddr_in from_addr;
        socklen_t from_len = sizeof(from_addr);
        ssize_t n = recvfrom(sockfd, recv_buf, (size_t)packet_size, 0,
                             (struct sockaddr *)&from_addr, &from_len);
        if (n >= (ssize_t)sizeof(PacketHeader)) {
            uint64_t recv_time = now_ns();
            double rtt_ms = (double)(recv_time - send_time) / 1e6;
            bytes_received_window += (uint64_t)n;
            total_bytes_received += (uint64_t)n;
            delay_sum_ms_window += rtt_ms;
            total_delay_ms += rtt_ms;
            delay_samples_window++;
            total_received++;
        }

        uint64_t tnow = now_ns();
        while (tnow >= next_window_ns) {
            double throughput_mbps = ((double)bytes_received_window * 8.0) / 1000000.0;
            double avg_delay_ms = delay_samples_window > 0 ? delay_sum_ms_window / (double)delay_samples_window : 0.0;

            fprintf(f_thr, "%d,%.6f\n", second_idx, throughput_mbps);
            fprintf(f_dly, "%d,%.6f\n", second_idx, avg_delay_ms);

            printf("sec=%d throughput=%.3f Mbps avg_delay=%.3f ms samples=%d\n",
                   second_idx, throughput_mbps, avg_delay_ms, delay_samples_window);

            second_idx++;
            bytes_received_window = 0;
            delay_sum_ms_window = 0.0;
            delay_samples_window = 0;
            next_window_ns += 1000000000ULL;
        }

        sleep_us(interval_us);
    }

    fclose(f_thr);
    fclose(f_dly);

    double avg_delay_total = total_received > 0 ? total_delay_ms / (double)total_received : 0.0;
    double duration = (double)duration_sec;
    double avg_throughput = duration > 0 ? ((double)total_bytes_received * 8.0) / (duration * 1000000.0) : 0.0;
    double loss_pct = total_sent > 0 ? (double)(total_sent - total_received) * 100.0 / (double)total_sent : 0.0;

    printf("\n--- Throughput Summary ---\n");
    printf("Sent=%d Received=%d Loss=%.2f%%\n", total_sent, total_received, loss_pct);
    printf("Average throughput: %.3f Mbps\n", avg_throughput);
    printf("Average delay: %.3f ms\n", avg_delay_total);
    printf("CSV outputs: %s, %s\n", throughput_path, delay_path);

    free(send_buf);
    free(recv_buf);
    close(sockfd);
    return 0;
}
