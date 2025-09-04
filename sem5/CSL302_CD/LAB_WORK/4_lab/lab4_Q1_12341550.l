%{
	#include<stdio.h>
	#include<string.h>
%}

%%

"cat"[ \t]+[a-zA-Z0-9_./-]+ {
    char filename[100];
    sscanf(yytext, "cat %s", filename);
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("Error opening file");
    } else {
        char c;
        while ((c = fgetc(fp)) != EOF) {
            putchar(c);
        }
        fclose(fp);
    }
}

"head"[ \t]+[a-zA-Z0-9_./-]+ {
    char filename[100];
    sscanf(yytext, "head %s", filename);
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("Error opening file");
    } else {
        char line[256];
        int count = 0;
        while (fgets(line, sizeof(line), fp) && count < 10) {
            printf("%s", line);
            count++;
        }
        fclose(fp);
    }
}

"tail"[ \t]+[a-zA-Z0-9_./-]+ {
    char filename[100];
    sscanf(yytext, "tail %s", filename);
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("Error opening file");
    } else {
        char *lines[10];
        char buffer[256];
        int i = 0;
        for(int j=0; j<10; ++j) lines[j] = NULL;

        while(fgets(buffer, sizeof(buffer), fp)) {
            if(lines[i]) free(lines[i]);
            lines[i] = strdup(buffer);
            i = (i + 1) % 10;
        }

        int start = i;
        for(int j=0; j<10; ++j) {
            int current = (start + j) % 10;
            if(lines[current]) {
                printf("%s", lines[current]);
                free(lines[current]);
            }
        }
        fclose(fp);
    }
}

"cp"[ \t]+[a-zA-Z0-9_./-]+[ \t]+[a-zA-Z0-9_./-]+ {
    char src[100], dest[100];
    sscanf(yytext, "cp %s %s", src, dest);
    FILE *source = fopen(src, "r");
    if (source == NULL) {
        perror("Error opening source file");
    } else {
        FILE *destination = fopen(dest, "w");
        if (destination == NULL) {
            perror("Error opening destination file");
            fclose(source);
        } else {
            char c;
            while ((c = fgetc(source)) != EOF) {
                fputc(c, destination);
            }
            printf("File copied successfully.\n");
            fclose(destination);
            fclose(source);
        }
    }
}

.+ { printf("Invalid command\n"); }

%%

int yywrap(){
	return 1;
}

int main(void){
    printf("Enter command (e.g., cat <filename>, cp <src> <dest>, head <filename>, tail <filename>):\n");
	yylex();
    return 0;
}
