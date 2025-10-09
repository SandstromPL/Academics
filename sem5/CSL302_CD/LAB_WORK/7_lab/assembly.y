%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);
%}


%token MOV ADD SUB MUL DIV LOAD STORE JMP CMP HALT
%token LABEL REGISTER IMMEDIATE_NUMBER
%token COMMA SEMI_COLON COLON


%union {
    char* str;
}

%start program
%type <str> FIRST_ARITH


%%
program:
	statements
	;

statements:
	statement
	| statement statements
	| LABEL COLON statement
	;

statement:
	arithmetic
	| conditional
	| memory
	| halt
	;

arithmetic:
	FIRST_ARITH REGISTER COMMA REGISTER
	| FIRST_ARITH REGISTER COMMA IMMEDIATE_NUMBER
	;

FIRST_ARITH:
	MOV
	| ADD
	| SUB
	| MUL
	| DIV
	;
conditional:
	JMP LABEL
	;

memory:
	LOAD REGISTER COMMA IMMEDIATE_NUMBER
	| STORE REGISTER COMMA IMMEDIATE_NUMBER
	;
	
halt:
	HALT

%%

int main() {
    printf("\nStart assembly code...\n");
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

