#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define MAX_DGRAM_SIZE 65507

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <listen_port>\n", argv[0]);
        return 1;
    }

    int port = atoi(argv[1]);
    if (port <= 0 || port > 65535) {
        fprintf(stderr, "Invalid port: %s\n", argv[1]);
        return 1;
    }

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket");
        return 1;
    }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons((uint16_t)port);

    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("bind");
        close(sockfd);
        return 1;
    }

    printf("UDP Echo Server listening on port %d\n", port);

    unsigned char *buffer = (unsigned char *)malloc(MAX_DGRAM_SIZE);
    if (buffer == NULL) {
        fprintf(stderr, "Failed to allocate buffer\n");
        close(sockfd);
        return 1;
    }

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        ssize_t bytes = recvfrom(sockfd, buffer, MAX_DGRAM_SIZE, 0,
                                 (struct sockaddr *)&client_addr, &client_len);
        if (bytes < 0) {
            if (errno == EINTR) {
                continue;
            }
            perror("recvfrom");
            break;
        }

        ssize_t sent = sendto(sockfd, buffer, (size_t)bytes, 0,
                              (struct sockaddr *)&client_addr, client_len);
        if (sent < 0) {
            perror("sendto");
            break;
        }
    }

    free(buffer);
    close(sockfd);
    return 0;
}
