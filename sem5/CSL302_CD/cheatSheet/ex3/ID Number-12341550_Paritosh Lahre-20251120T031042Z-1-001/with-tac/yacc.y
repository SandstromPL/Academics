%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symbol.h"

void yyerror(const char *s);
int yylex(void);

/* Helper to check semantics without triggering "Redeclaration" error on assignments */
void check_and_install(char* name, char* type) {
    if (lookupSymbol(name) == NULL) {
        insertSymbol(name, type, 0);
    }
}

/* Helper to verify usage */
void check_defined(char* name) {
    if (lookupSymbol(name) == NULL) {
        printf("Semantic Error: Variable '%s' used but not defined.\n", name);
    }
}

%}

%token IF GOTO
%token <str> IDENTIFIER TEMP_VAR CONSTANT LABEL
%token PLUS MINUS MULTIPLY DIVIDE LT GT ASSGN NEG EQ NE LE GE
%token LEFT_SQUARE RIGHT_SQUARE SEMICOLON COLON

%union {
    char* str;
}

%start PROGRAM

/* Types for semantic values */
%type <str> LVAL RVAL EXPR REL_OP

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
    LVAL ASSGN EXPR {
        /* Semantic Action: Validate Assignment */
        printf("TAC: %s = %s\n", $1, $3);
    }
    | PRE_OPT LVAL ASSGN EXPR {
        /* Semantic Action: Validate Labeled Assignment */
        printf("TAC: %s = %s (Labeled)\n", $2, $4);
    }
    ;

LVAL:
    IDENTIFIER { 
        check_and_install($1, "id"); 
        $$ = $1; 
    }
    | TEMP_VAR { 
        check_and_install($1, "temp"); 
        $$ = $1; 
    }
    ;

RVAL:
    IDENTIFIER { 
        /* In strict semantics, we would define check_defined($1) here. 
           For this lab, we usually just pass it through. */
        check_and_install($1, "id"); /* Auto-install for simplicity in TAC parsing */
        $$ = $1; 
    }
    | TEMP_VAR { 
        check_and_install($1, "temp");
        $$ = $1; 
    }
    | CONSTANT { 
        $$ = $1; 
    }
    ;

EXPR:
    RVAL { $$ = $1; }
    | RVAL PLUS RVAL      { char* s = malloc(20); sprintf(s, "%s + %s", $1, $3); $$ = s; }
    | RVAL MINUS RVAL     { char* s = malloc(20); sprintf(s, "%s - %s", $1, $3); $$ = s; }
    | RVAL MULTIPLY RVAL  { char* s = malloc(20); sprintf(s, "%s * %s", $1, $3); $$ = s; }
    | RVAL DIVIDE RVAL    { char* s = malloc(20); sprintf(s, "%s / %s", $1, $3); $$ = s; }
    | MINUS RVAL %prec UMINUS { char* s = malloc(20); sprintf(s, "-%s", $2); $$ = s; }
    | NEG RVAL %prec NEGATE   { char* s = malloc(20); sprintf(s, "!%s", $2); $$ = s; }
    | RVAL LEFT_SQUARE RVAL RIGHT_SQUARE { char* s = malloc(40); sprintf(s, "%s[%s]", $1, $3); $$ = s; }
    | MULTIPLY RVAL %prec MUL { char* s = malloc(20); sprintf(s, "*%s", $2); $$ = s; }
    ;

CONDITIONAL:
    IF LVAL REL_OP LVAL GOTO LABEL {
        printf("TAC: if %s %s %s goto %s\n", $2, $3, $4, $6);
    }
    | GOTO LABEL {
        printf("TAC: goto %s\n", $2);
    }
    | PRE_OPT IF LVAL REL_OP LVAL GOTO LABEL {
        printf("TAC: if %s %s %s goto %s (Labeled)\n", $3, $4, $5, $7);
    }
    ;

REL_OP:
    GT  { $$ = ">"; }
    | LT { $$ = "<"; }
    | LE { $$ = "<="; }
    | GE { $$ = ">="; }
    | EQ { $$ = "=="; }
    | NE { $$ = "!="; }
    ;

PRE_OPT:
    LABEL COLON { 
        printf("Label Defined: %s\n", $1); 
    }
    ;

%%

int main(void) {
    printf("Enter TAC code:\n");
    int result = yyparse();
    if (result == 0){
        printf("\nParsing successful\n");
    } else {
        printf("\nParsing failed\n");
    }
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
