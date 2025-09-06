%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);
%}

%token INT FLOAT CHAR
%token FOR_WORD
%token IDENTIFIER
%token SEMICOLON
%token COMMA
%token EQUAL
%token LEFT_BRAC RIGHT_BRAC

%union {
    char* str;
}

%start program
%type <str> IDENTIFIER
%type <str> EXPRESSION
%type <str> DATATYPE
%type <str> IDENTIFIERS
%type <str> LEFT_BRAC
%type <str> RIGHT_BRAC

%left '*' '/' '%'
%left '+' '-'


%%
program:
    declarations
    ;

declarations:
    declarations declaration
    | declaration
    ;

declaration:
    DATATYPE IDENTIFIER SEMICOLON {
        printf("Declared variable: %s of type %s\n", $2, $1);
        free($2);
        free($1);
    }
    | DATATYPE IDENTIFIERS SEMICOLON {
	printf("Declared multiple variables: %s of type %s\n", $2, $1);
	free($2);
	free($1);
    }
    | ASSIGNMENT_SENTENCE SEMICOLON
    | FOR_LOOP SEMICOLON
    ;

ASSIGNMENT_SENTENCE:
    IDENTIFIER EQUAL EXPRESSION {
	printf("Mathematical Expression assigned to variable %s\n", $1);
	free($1);
    }
    ;

IDENTIFIERS: 
    IDENTIFIERS COMMA IDENTIFIER {
	$$ = strdup($1);
	char space[] = " ";
	memmove($$ + strlen($$), space, strlen(space) + 1);
	memmove($$ + strlen($$), $3, strlen($3) + 1);
    }
    | IDENTIFIER COMMA IDENTIFIER {
	$$ = strdup($1);
	char space[] = " ";
	memmove($$ + strlen($$), space, strlen(space) + 1);
	memmove($$ + strlen($$), $3, strlen($3) + 1);
    }
    ;

DATATYPE:
    INT     { $$ = strdup("int"); }
    | FLOAT { $$ = strdup("float"); }
    | CHAR  { $$ = strdup("char"); }
    ;

EXPRESSION:
    EXPRESSION'+'EXPRESSION
    | EXPRESSION'-'EXPRESSION
    | EXPRESSION'*'EXPRESSION
    | EXPRESSION'/'EXPRESSION
    | EXPRESSION'%'EXPRESSION
    | LEFT_BRAC EXPRESSION RIGHT_BRAC
    | IDENTIFIER
    ;

FOR_LOOP:
    FOR_WORD LEFT_BRAC EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHT_BRAC ASSIGNMENT_SENTENCE{
	printf("FOR LOOP DETECTED\n");
    }
    ;
%%

int main() {
    printf("\nEnter Any Arithmetic Expression with operations Addition, Subtraction, Multiplication, Division, Modulus and Round brackets\n");
    printf("Or enter variable declarations\n");
    printf("Or FOR loop:\n");
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

