%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex();
void yyerror(const char* s) { fprintf(stderr, "Error: %s\n", s); }
%}

/* Define possible value types */
%union {
    int ival;
    float fval;
    char* sval;
}

/* Token declarations */
%token <ival> INT
%token <fval> FLOAT
%token <sval> ID

/* Non-terminal type declarations */
%type <ival> expr
%type <fval> fexpr

%%

program:
    program stmt
  | stmt
  ;

stmt:
    expr ';'     { printf("Integer expression result: %d\n", $1); }
  | fexpr ';'    { printf("Float expression result: %f\n", $1); }
  | ID '=' expr ';'  { printf("Assign %s = %d\n", $1, $3); free($1); }
  | ID '=' fexpr ';' { printf("Assign %s = %f\n", $1, $3); free($1); }
  ;

expr:
    INT                  { $$ = $1; }
  | expr '+' expr        { $$ = $1 + $3; }
  | expr '*' expr        { $$ = $1 * $3; }
  ;

fexpr:
    FLOAT                { $$ = $1; }
  | fexpr '+' fexpr      { $$ = $1 + $3; }
  | fexpr '*' fexpr      { $$ = $1 * $3; }
  ;

%%

int main() {
    printf("Enter expressions:\n");
    yyparse();
    return 0;
}

