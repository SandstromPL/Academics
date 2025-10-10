%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);
%}

%union {
    char* str;
}

%token MOV ADD SUB MUL DIV LOAD STORE JMP CMP HALT
%token <str> LABEL REGISTER IMMEDIATE_NUMBER
%token COMMA SEMI_COLON COLON



%start program
%type <str> FIRST_ARITH


%%
program:
	statements
	;

statements:
	statement
	| statement statements
	;

statement:
	optional arithmetic
	| optional conditional
	| optional memory
	| halt
	;
optional:
	/**/
	| LABEL COLON
	;
arithmetic:
	FIRST_ARITH REGISTER COMMA REGISTER
	{
		printf("ARITHMETIC STATEMENT called successfuly.\n");
	}
	| FIRST_ARITH REGISTER COMMA IMMEDIATE_NUMBER
	{
		printf("ARITHMETIC STATEMENT called successfuly.\n");
	}
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
	{
		printf("CONDITIONAL STATEMENT called successfuly.\n");
	}
	;

memory:
	LOAD REGISTER COMMA IMMEDIATE_NUMBER
	{
		printf("MEMORY STATEMENT called successfuly.\n");
	}
	| STORE REGISTER COMMA IMMEDIATE_NUMBER
	{
		printf("MEMORY STATEMENT called successfuly.\n");
	}
	;
	
halt:
	HALT
	{
		printf("HALT encountered. Program execution stopped.\n");
        	exit(0);
	}
	;

%%

int main() {
    printf("\nStart assembly code...\n");
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

