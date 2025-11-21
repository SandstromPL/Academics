%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);
%}

%token IF GOTO
%token IDENTIFIER TEMP_VAR CONSTANT LABEL
%token PLUS MINUS MULTIPLY DIVIDE LT GT ASSGN NEG EQ NE LE GE
%token LEFT_SQUARE RIGHT_SQUARE SEMICOLON COLON

%union {
    char* str;
}

%start PROGRAM
%type <str> IDENTIFIER
%type <str> TEMP_VAR
%type <str> CONSTANT
%type <str> LABEL
%type <str> LEFT_SQUARE
%type <str> RIGHT_SQUARE

%right ASSGN
%nonassoc EQ NE
%nonassoc LT GT LE GE
%left PLUS MINUS
%left MULTIPLY DIVIDE
%right UMINUS NEGATE MUL
%left LEFT_SQUARE RIGHT_SQUARE


%%

PROGRAM:
    STATEMENTS
    ;

STATEMENTS:
    STATEMENTS STATEMENT
    | STATEMENT
    ;

STATEMENT:
    ARITMETIC
    | CONDITIONAL
    ;

ARITMETIC:
    LVAL ASSGN EXPR
    | PRE_OPT LVAL ASSGN EXPR
    ;

LVAL:
    IDENTIFIER
    | TEMP_VAR
    ;

RVAL:
    IDENTIFIER
    | TEMP_VAR
    |CONSTANT
    ;

EXPR:
    RVAL
    | RVAL PLUS RVAL
    | RVAL MINUS RVAL
    | RVAL MULTIPLY RVAL
    | RVAL DIVIDE RVAL
    | MINUS RVAL %prec UMINUS
    | NEG RVAL %prec NEGATE
    | RVAL LEFT_SQUARE RVAL RIGHT_SQUARE
    | MULTIPLY RVAL %prec MUL 
    ;

CONDITIONAL:
    IF LVAL REL_OP LVAL GOTO LABEL
    | GOTO LABEL
    | PRE_OPT IF LVAL REL_OP LVAL GOTO LABEL
    ;

REL_OP:
    GT
    | LT
    | LE
    | GE
    | EQ
    | NE
    ;

PRE_OPT:
    LABEL COLON
    ;
%%

int main(void) {

    printf("Enter code here:\n");
    int result = yyparse();
    if (result == 0){
        printf("Parsing successful\n");
    }else{
        printf("Parsing failed\n");
    }
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}