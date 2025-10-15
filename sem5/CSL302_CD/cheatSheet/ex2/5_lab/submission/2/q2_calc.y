%{
#include<stdio.h>
int yylex(void);
void yyerror(const char *s);
int sym[26];
%}

%union {
    int val;
    int index;
}

%start lines
%token <val> NUMBER
%token <index> IDENTIFIER
%token SEMICOLON
%token FOR

%type <val> E

%left '+' '-' '%'
%left '*' '/'
%left '(' ')'
%left '<'

%%

lines:
    lines statement ';' { printf("\n"); }
    |
    ;

statement:
    assignment_statement
    | E                  { printf("\nResult = %d", $1); }
    | FOR '(' E ';' E ';' E ')' assignment_statement { printf("Valid for loop"); }
    ;

assignment_statement:
    IDENTIFIER '=' E     { sym[$1 - 'a'] = $3; printf("Valid assignment"); }
    ;

E:
    E '+' E              { $$ = $1 + $3; }
    | E '-' E            { $$ = $1 - $3; }
    | E '*' E            { $$ = $1 * $3; }
    | E '/' E            { if($3) $$ = $1 / $3; else yyerror("divide by zero"); }
    | E '<' E            { $$ = $1 < $3; }
    | IDENTIFIER '=' E   { sym[$1 - 'a'] = $3; $$ = $3; }
    | '(' E ')'          { $$ = $2; }
    | NUMBER
    | IDENTIFIER         { $$ = sym[$1 - 'a']; }
    ;

%%

int main() {
    printf("Enter expression(s):\n");
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Invalid\n");
}
