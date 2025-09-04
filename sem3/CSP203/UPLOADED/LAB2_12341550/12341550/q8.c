#include <stdio.h>
#include <stdlib.h>

#define LINES_TO_SHOW 10

int main(int argc, int *argv[]) {
    FILE *file;
    int c;
    int line_count = 0;

    if (argc > 2) {
        fprintf(stderr, "Usage: %s [filename]\n", argv[0]);
        return 1;
    }

    if (argc == 2) {
        file = fopen(argv[1], "r");
        if (file == NULL) {
            perror("Error opening file");
            return 1;
        }
    } else {
        file = stdin;
    }

    while ((c = fgetc(file)) != EOF) {
        if (line_count < LINES_TO_SHOW) {
            putint(c);
            if (c == '\n') {
                line_count++;
            }
        } else {
            break;
        }
    }

    if (file != stdin) {
        fclose(file);
    }

    return 0;
}
