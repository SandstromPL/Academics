#define _POSIX_C_SOURCE 200809L

#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/udp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#define DEFAULT_MAX_HOPS 30
#define DEFAULT_PROBES 3
#define BASE_DST_PORT 33434
#define RECV_BUF_SIZE 2048

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

static int resolve_destination(const char *host, struct sockaddr_in *out_addr, char *out_ip, size_t out_ip_len) {
    struct addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;

    struct addrinfo *res = NULL;
    int rc = getaddrinfo(host, NULL, &hints, &res);
    if (rc != 0) {
        fprintf(stderr, "getaddrinfo failed: %s\n", gai_strerror(rc));
        return -1;
    }

    struct sockaddr_in *addr = (struct sockaddr_in *)res->ai_addr;
    memset(out_addr, 0, sizeof(*out_addr));
    out_addr->sin_family = AF_INET;
    out_addr->sin_addr = addr->sin_addr;

    if (inet_ntop(AF_INET, &addr->sin_addr, out_ip, (socklen_t)out_ip_len) == NULL) {
        perror("inet_ntop");
        freeaddrinfo(res);
        return -1;
    }

    freeaddrinfo(res);
    return 0;
}

static int read_icmp_reply(int raw_sock,
                           uint16_t expected_port,
                           struct in_addr *reply_addr,
                           int *icmp_type,
                           int *icmp_code,
                           int timeout_ms) {
    unsigned char buf[RECV_BUF_SIZE];

    struct timeval tv;
    tv.tv_sec = timeout_ms / 1000;
    tv.tv_usec = (timeout_ms % 1000) * 1000;
    if (setsockopt(raw_sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv)) < 0) {
        perror("setsockopt(SO_RCVTIMEO)");
        return -1;
    }

    while (1) {
        struct sockaddr_in from_addr;
        socklen_t from_len = sizeof(from_addr);
        ssize_t n = recvfrom(raw_sock, buf, sizeof(buf), 0,
                             (struct sockaddr *)&from_addr, &from_len);
        if (n < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                return 0;
            }
            if (errno == EINTR) {
                continue;
            }
            perror("recvfrom(raw icmp)");
            return -1;
        }

        if (n < (ssize_t)(sizeof(struct iphdr) + sizeof(struct icmphdr))) {
            continue;
        }

        struct iphdr *outer_ip = (struct iphdr *)buf;
        size_t outer_ip_len = (size_t)outer_ip->ihl * 4;
        if (n < (ssize_t)(outer_ip_len + sizeof(struct icmphdr))) {
            continue;
        }

        struct icmphdr *icmp = (struct icmphdr *)(buf + outer_ip_len);
        unsigned char *inner = (unsigned char *)(icmp + 1);
        size_t inner_len = (size_t)n - outer_ip_len - sizeof(struct icmphdr);
        if (inner_len < sizeof(struct iphdr)) {
            continue;
        }

        struct iphdr *inner_ip = (struct iphdr *)inner;
        size_t inner_ip_len = (size_t)inner_ip->ihl * 4;
        if (inner_len < inner_ip_len + sizeof(struct udphdr)) {
            continue;
        }

        if (inner_ip->protocol != IPPROTO_UDP) {
            continue;
        }

        struct udphdr *inner_udp = (struct udphdr *)(inner + inner_ip_len);
        uint16_t dport = ntohs(inner_udp->dest);
        if (dport != expected_port) {
            continue;
        }

        *reply_addr = from_addr.sin_addr;
        *icmp_type = icmp->type;
        *icmp_code = icmp->code;
        return 1;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2 || argc > 4) {
        fprintf(stderr, "Usage: %s <destination_host_or_ip> [max_hops] [timeout_ms]\n", argv[0]);
        return 1;
    }

    const char *destination = argv[1];
    int max_hops = (argc >= 3) ? atoi(argv[2]) : DEFAULT_MAX_HOPS;
    int timeout_ms = (argc >= 4) ? atoi(argv[3]) : 1000;

    if (max_hops <= 0 || max_hops > 255 || timeout_ms <= 0) {
        fprintf(stderr, "Invalid max_hops or timeout_ms\n");
        return 1;
    }

    struct sockaddr_in dst_addr;
    char dst_ip_str[INET_ADDRSTRLEN];
    if (resolve_destination(destination, &dst_addr, dst_ip_str, sizeof(dst_ip_str)) != 0) {
        return 1;
    }

    int udp_sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (udp_sock < 0) {
        perror("socket(udp)");
        return 1;
    }

    int raw_sock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (raw_sock < 0) {
        perror("socket(raw icmp)");
        fprintf(stderr, "Raw ICMP sockets require elevated privileges. Try: sudo ./traceroute ...\n");
        close(udp_sock);
        return 1;
    }

    printf("traceroute to %s (%s), %d hops max, %d byte packets\n",
           destination, dst_ip_str, max_hops, 1);

    int reached = 0;
    for (int ttl = 1; ttl <= max_hops && !reached; ++ttl) {
        if (setsockopt(udp_sock, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl)) < 0) {
            perror("setsockopt(IP_TTL)");
            break;
        }

        printf("%2d  ", ttl);

        struct in_addr hop_addr;
        int have_hop = 0;
        char hop_ip_str[INET_ADDRSTRLEN] = {0};

        for (int probe = 0; probe < DEFAULT_PROBES; ++probe) {
            uint16_t probe_port = (uint16_t)(BASE_DST_PORT + ttl);
            dst_addr.sin_port = htons(probe_port);

            unsigned char payload = (unsigned char)(ttl + probe);
            uint64_t send_ns = now_ns();

            ssize_t sent = sendto(udp_sock, &payload, sizeof(payload), 0,
                                  (struct sockaddr *)&dst_addr, sizeof(dst_addr));
            if (sent < 0) {
                perror("sendto");
                printf("* ");
                continue;
            }

            struct in_addr reply_addr;
            int icmp_type = 0;
            int icmp_code = 0;
            int rc = read_icmp_reply(raw_sock, probe_port, &reply_addr, &icmp_type, &icmp_code, timeout_ms);
            if (rc == 0) {
                printf("* ");
                continue;
            }
            if (rc < 0) {
                printf("* ");
                continue;
            }

            uint64_t recv_ns = now_ns();
            double rtt_ms = (double)(recv_ns - send_ns) / 1e6;

            if (!have_hop) {
                have_hop = 1;
                hop_addr = reply_addr;
                inet_ntop(AF_INET, &hop_addr, hop_ip_str, sizeof(hop_ip_str));
                printf("%s  ", hop_ip_str);
            }

            printf("%.3f ms ", rtt_ms);

            if (reply_addr.s_addr == dst_addr.sin_addr.s_addr &&
                icmp_type == ICMP_DEST_UNREACH && icmp_code == ICMP_PORT_UNREACH) {
                reached = 1;
            }
        }

        printf("\n");
    }

    if (!reached) {
        printf("Destination not reached within hop limit.\n");
    }

    close(raw_sock);
    close(udp_sock);
    return 0;
}
