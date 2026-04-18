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
} EchoHeader;
#pragma pack(pop)

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

static void sleep_ms(int ms) {
    struct timespec req;
    req.tv_sec = ms / 1000;
    req.tv_nsec = (long)(ms % 1000) * 1000000L;
    nanosleep(&req, NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 6) {
        fprintf(stderr, "Usage: %s <server_ip> <port> <num_packets> <packet_size_bytes> <interval_ms>\n", argv[0]);
        return 1;
    }

    const char *server_ip = argv[1];
    int port = atoi(argv[2]);
    int num_packets = atoi(argv[3]);
    int packet_size = atoi(argv[4]);
    int interval_ms = atoi(argv[5]);

    if (port <= 0 || port > 65535 || num_packets <= 0 || packet_size < (int)sizeof(EchoHeader) || packet_size > 65507 || interval_ms < 0) {
        fprintf(stderr, "Invalid arguments\n");
        return 1;
    }

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket");
        return 1;
    }

    struct timeval timeout;
    timeout.tv_sec = 1;
    timeout.tv_usec = 0;
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
        fprintf(stderr, "Invalid server IP: %s\n", server_ip);
        close(sockfd);
        return 1;
    }

    unsigned char *send_buf = (unsigned char *)malloc((size_t)packet_size);
    unsigned char *recv_buf = (unsigned char *)malloc((size_t)packet_size);
    if (send_buf == NULL || recv_buf == NULL) {
        fprintf(stderr, "Failed to allocate packet buffers\n");
        free(send_buf);
        free(recv_buf);
        close(sockfd);
        return 1;
    }

    double total_rtt_ms = 0.0;
    int received = 0;

    printf("Sending %d packets to %s:%d, packet_size=%d bytes, interval=%d ms\n",
           num_packets, server_ip, port, packet_size, interval_ms);

    for (int i = 0; i < num_packets; ++i) {
        memset(send_buf, 'A' + (i % 26), (size_t)packet_size);
        EchoHeader *hdr = (EchoHeader *)send_buf;
        hdr->seq = htonl((uint32_t)i);
        hdr->send_ts_ns = now_ns();

        uint64_t send_time_ns = now_ns();
        ssize_t sent = sendto(sockfd, send_buf, (size_t)packet_size, 0,
                              (struct sockaddr *)&server_addr, sizeof(server_addr));
        if (sent < 0) {
            perror("sendto");
            break;
        }

        struct sockaddr_in from_addr;
        socklen_t from_len = sizeof(from_addr);
        ssize_t n = recvfrom(sockfd, recv_buf, (size_t)packet_size, 0,
                             (struct sockaddr *)&from_addr, &from_len);

        if (n < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                printf("seq=%d timeout\n", i);
            } else {
                perror("recvfrom");
            }
        } else if (n >= (ssize_t)sizeof(EchoHeader)) {
            EchoHeader *rh = (EchoHeader *)recv_buf;
            uint32_t seq = ntohl(rh->seq);
            uint64_t recv_time_ns = now_ns();
            double rtt_ms = (double)(recv_time_ns - send_time_ns) / 1e6;
            total_rtt_ms += rtt_ms;
            received++;
            printf("seq=%u bytes=%zd rtt=%.3f ms\n", seq, n, rtt_ms);
        } else {
            printf("seq=%d invalid_reply_size=%zd\n", i, n);
        }

        if (i != num_packets - 1 && interval_ms > 0) {
            sleep_ms(interval_ms);
        }
    }

    int lost = num_packets - received;
    double loss_pct = ((double)lost * 100.0) / (double)num_packets;
    double avg_rtt = received > 0 ? total_rtt_ms / (double)received : 0.0;

    printf("\n--- RTT Summary ---\n");
    printf("Packets: sent=%d received=%d lost=%d (%.2f%% loss)\n", num_packets, received, lost, loss_pct);
    printf("Average RTT: %.3f ms\n", avg_rtt);

    free(send_buf);
    free(recv_buf);
    close(sockfd);
    return 0;
}
