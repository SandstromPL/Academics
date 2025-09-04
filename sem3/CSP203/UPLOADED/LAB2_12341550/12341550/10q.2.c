#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <dst> <src>\n", argv[0]);
        return 1;
    }

    FILE *src = fopen(argv[2], "r");
    if (src == NULL) {
        perror("Error opening source file");
        return 1;
    }

    FILE *dst = fopen(argv[1], "w");
    if (dst == NULL) {
        perror("Error opening destination file");
        fclose(src);
        return 1;
    }

    char buffer[BUFSIZ];
    size_t bytesRead;
    while ((bytesRead = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        fwrite(buffer, 1, bytesRead, dst);
    }

    fclose(src);
    fclose(dst);
    return 0;
}
