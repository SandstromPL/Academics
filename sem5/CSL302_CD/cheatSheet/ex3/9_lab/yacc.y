%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symbol.h"

int temp_count = 1;
char* current_type;

char* new_temp() {
    char *temp = (char*)malloc(12);
    sprintf(temp, "t%d", temp_count++);
    return temp;
}

void yyerror(const char *s);
int yylex(void);

%}

%union {
    char *str;
}

%token <str> ID
%token <str> NUM
%token ASSIGN PLUS MINUS MULTIPY DIVIDE LBRAC RBRAC LCURL RCURL
%token LT GT LE GE NE EQ
%token AND OR NOT TRUE FALSE IF ELSE THEN WHILE
%token INT FLOAT COMMA SEMICOLON

%type <str> expr

%start program
%right ASSIGN
%left PLUS MINUS
%left MULTIPY DIVIDE
%nonassoc LT GT LE GE NE EQ
%left OR
%left AND
%right NOT
%left LBRAC RBRAC

%%

program :
    stmts
    ;

stmts   : stmts stmt
        | /*  */
        ;

stmt    : declaration
        | assignment
        ;


assignment: ID ASSIGN expr SEMICOLON {
        printf("%s = %s\n", $1, $3);
    }
    ;

declaration : type id_list SEMICOLON
            ;

type        : INT   { current_type = "int"; }
            | FLOAT { current_type = "float"; }
            ;

id_list     : ID {
                insertSymbol($1, current_type, 0); 
            }
            | id_list COMMA ID {
                insertSymbol($3, current_type, 0);
            }
            ;

expr: expr PLUS expr {
        char *temp = new_temp();
        printf("%s = %s + %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr MINUS expr {
        char *temp = new_temp();
        printf("%s = %s - %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr MULTIPY expr {
        char *temp = new_temp();
        printf("%s = %s * %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr DIVIDE expr {
        char *temp = new_temp();
        printf("%s = %s / %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr LT expr {
        char *temp = new_temp();
        printf("%s = %s < %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr GT expr {
        char *temp = new_temp();
        printf("%s = %s > %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr LE expr {
        char *temp = new_temp();
        printf("%s = %s <= %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr GE expr {
        char *temp = new_temp();
        printf("%s = %s >= %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr EQ expr {
        char *temp = new_temp();
        printf("%s = %s == %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr NE expr {
        char *temp = new_temp();
        printf("%s = %s != %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr AND expr {
        char *temp = new_temp();
        printf("%s = %s and %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    expr OR expr {
        char *temp = new_temp();
        printf("%s = %s or %s\n", temp, $1, $3);
        $$ = temp;
    }
    |
    NOT expr {
        char *temp = new_temp();
        printf("%s = not %s\n", temp, $2);
        $$ = temp;
    }
    | TRUE {
        $$ = "true";
    }
    | FALSE {
        $$ = "false";
    }
    | LBRAC expr RBRAC {
        $$ = $2;
    }
    | ID {
        $$ = $1;
    }
    | NUM {
        $$ = $1;
    }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Enter program (declarations or assignments ending with ;):\n");
    yyparse();
    return 0;
}