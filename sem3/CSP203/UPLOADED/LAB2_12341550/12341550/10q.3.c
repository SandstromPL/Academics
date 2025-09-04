#include <stdio.h>
#include <stdlib.h>

#define DEFAULT_NUM_LINES 10

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <num> <file>\n", argv[0]);
        return 1;
    }

    int numLines = atoi(argv[1]);
    if (numLines <= 0) {
        fprintf(stderr, "Invalid number of lines: %d\n", numLines);
        return 1;
    }

    FILE *file = fopen(argv[2], "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    char line[BUFSIZ];
    int count = 0;
    while (fgets(line, sizeof(line), file) != NULL && count < numLines) {
        fputs(line, stdout);
        count++;
    }

    fclose(file);
    return 0;
}
