#include <stdio.h>
#include <stdlib.h>

#define DEFAULT_NUM_LINES 10


#define MAX_LINES 1000

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

    char *lines[MAX_LINES];
    int lineCount = 0;
    char line[BUFSIZ];

    while (fgets(line, sizeof(line), file) != NULL) {
        if (lineCount == MAX_LINES) {
            free(lines[0]);
            for (int i = 1; i < MAX_LINES; i++) {
                lines[i - 1] = lines[i];
            }
            lineCount--;
        }
        lines[lineCount] = strdup(line);
        lineCount++;
    }

    fclose(file);

    int start = lineCount - numLines;
    if (start < 0) {
        start = 0;
    }

    for (int i = start; i < lineCount; i++) {
        fputs(lines[i], stdout);
        free(lines[i]);
    }

    return 0;
}
