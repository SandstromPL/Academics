{%
    #include<stdio.h>
    #include<string.h>
    extern FILE *yyin;
    int line_count = 0;
    int word_count = 0;
    int char_count = 0;
}%

%%
[A-Z]([a-z])*([ \t]*)([A-Z]([a-z])*) {printf("%s\tNAME\n",yytext);}
([0-9]{3}){2}("-")([0-9]{4}) {printf("%s\tPHONE_NUMBER\n",yytext);}
[a-zA-Z]([a-zA-Z0-9]+)("@")([a-z]+)(".")([a-z]+)(".")([a-z]*) {printf("%s\tEMAIL\n",yytext);}
[0-9]{4}([ \t]*([0-9]{4})){3} {printf("%s\tCREDIT_CARD\n",yytext);}
(([0|1|2]+[0-9]+|[3][0|1])("-"))([0|1]+[0-9]+)("-")([0-9]{2}|[0-9]{4}) {printf("%s\tDOB\n",yytext);}

\n          {line_count++; char_count++;}
[ \t]+      {char_count += yyleng;}
[^ \t\n]+   {word_count++; char_count += yyleng;}
.           {char_count++;}

\"[^\"]*\"         { printf("%s STRING_LITERAL\n", yytext); }

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


[/](([a-zA-Z0-9]+|"..")[/])*([a-zA-Z0-9]+\.(txt|dat))? {printf("The PATH : %s is VALID\n",yytext);}

[0-9]+\.[0-9]+([eE][+]?[0-9]+)? {printf("%s : DOUBLE\n",yytext);}

\/\*([^*]|\*+[^*/])*\*\/    { printf("C-style multiline comment: %s\n", yytext); }
\"\"\"([^\"\\]|\\.|\"{1,2}(?!"\"))*\"\"\"  { printf("Python triple-quote multiline: %s\n", yytext); }

"//"[^\n]* {printf("Single Line Comments : %s\n",yytext);}

[ \t\n]+ { /* ignore whitespace */ }
["]([^"]|\\(.|\n))*["] {printf("%s : STRING\n",yytext);}

%%


int main(int argc,char * argv[]){
    if(argc < 2){
        fprintf(stderr,"Usage: %s <inputfile>\n",argv[0]);
        return 1;
    }

    yyin = fopen(argv[1], "r");
    if(!yyin){
        perror("Error opening file");
        return 1;
    }

    yylex();

    printf("%d %d %d %s\n",line_count,word_count,char_count,argv[1]);

    fclose(yyin);
    return 0;
}
