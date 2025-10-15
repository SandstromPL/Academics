%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);
%}

%token INT FLOAT CHAR
%token IDENTIFIER
%token SEMICOLON

%union {
    char* str;
}

%start program
%type <str> IDENTIFIER
%type <str> datatype



%%
program:
    declarations
    ;

declarations:
    declarations declaration
    | declaration
    ;

declaration:
    datatype IDENTIFIER SEMICOLON {
        printf("Declared variable: %s of type %s\n", $2, $1);
        free($2);
        free($1);
    }
    ;

datatype:
    INT     { $$ = strdup("int"); }
    | FLOAT { $$ = strdup("float"); }
    | CHAR  { $$ = strdup("char"); }
    ;
%%

int main() {
    printf("Enter variable declarations:\n");
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

