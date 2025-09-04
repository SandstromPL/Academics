#include <stdio.h>

int main() {
    FILE *file;
    char c;
    int lines = 0, words = 0, chars = 0;
    int inWord = 0;

    file = fopen("1.c", "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    while ((c = fgetc(file)) != EOF) {
        chars++;
	//printf("%c\n",c);
        if (c == '\n') {
            lines++;
        }

        if (c == ' ' || c == '\n' || c == '\t' || c == '\r') {
            if (inWord) {
                inWord = 0;
                words++;
            }
        } else {
            inWord = 1;
        }
    }

    if (inWord) {
        words++;
    }

    fclose(file);

    printf("%d %d %d file.txt\n", lines, words, chars);

    return 0;
}
