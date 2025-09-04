#include <stdio.h>

int main() {
    FILE *file;
    char pattern[100];
    char filename[100];
    char line[1000];
    int lineNum = 1;

    printf("Enter the string pattern to search: ");
    scanf("%s", pattern);

    printf("Enter the file name: ");
    scanf("%s", filename);

    file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    while (fgets(line, sizeof(line), file)) {
        int i = 0, j = 0;
        int match = 0;

        while (line[i] != '\0' && pattern[j] != '\0') {
            if (line[i] == pattern[j]) {
                i++;
                j++;
            } else {
                i = i - j + 1;
                j = 0;
            }

            if (pattern[j] == '\0') {
                match = 1;
            }
        }

        if (match) {
            printf("%d: %s", lineNum, line);
        }

        lineNum++;
    }

    fclose(file);

    return 0;
}
