%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);
%}

%token INT FLOAT CHAR
%token FOR_WORD IF THEN ELSE ELIF WHILE DO
%token IDENTIFIER
%token SEMICOLON
%token COMMA
%token EQUAL NOT_EQUAL GRT_EQUAL LES_EQUAL GRT LES
%token LEFT_BRAC RIGHT_BRAC LEFT_CURL_BRAC RIGHT_CURL_BRAC
%token SWITCH CASE COLON

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
%type <str> LEFT_CURL_BRAC
%type <str> RIGHT_CURL_BRAC

%left NOT_EQUAL GRT_EQUAL LES_EQUAL GRT LES
%left '+' '-'
%left '*' '/' '%'


%%
program:
    STMTS
    ;

STMTS:
    STMTS STMT
    | STMT
    ;
    
BLOCK:
    LEFT_CURL_BRAC STMTS RIGHT_CURL_BRAC
    ;

STMT:
    declaration
    | ASSIGNMENT_SENTENCE SEMICOLON
    | IF_THEN
    | IF_THEN_ELSE
    | IF_THEN_ELIF
    | WHILE_LOOP
    | DO_WHILE_LOOP
    | FOR_LOOP SEMICOLON
    /* | SWITCH_CASE */
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
/*     | ASSIGNMENT_SENTENCE SEMICOLON
    | FOR_LOOP SEMICOLON
    | IF_THEN
    | IF_THEN_ELSE
    | IF_THEN_ELIF
    | WHILE_LOOP
    | DO_WHILE_LOOP */
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
    | EXPRESSION NOT_EQUAL EXPRESSION
    | EXPRESSION GRT_EQUAL EXPRESSION
    | EXPRESSION LES_EQUAL EXPRESSION
    | EXPRESSION GRT EXPRESSION
    | EXPRESSION LES EXPRESSION
    | IDENTIFIER
    ;

FOR_LOOP:
    FOR_WORD LEFT_BRAC EXPRESSION SEMICOLON EXPRESSION SEMICOLON EXPRESSION RIGHT_BRAC ASSIGNMENT_SENTENCE{
	printf("FOR LOOP DETECTED\n");
    }
    ;

IF_THEN:
   IF LEFT_BRAC EXPRESSION RIGHT_BRAC THEN BLOCK{
      printf("IF-THEN DETECTED\n");
   }
   ;

IF_THEN_ELSE:
   IF LEFT_BRAC EXPRESSION RIGHT_BRAC THEN BLOCK ELSE BLOCK{
      printf("IF-THEN-ELSE DETECTED\n");
   }
   ;

IF_THEN_ELIF:
   IF LEFT_BRAC EXPRESSION RIGHT_BRAC THEN BLOCK ELIF BLOCK ELSE BLOCK{
      printf("IF-THEN-ELIF DETECTED\n");
   }
   ;

WHILE_LOOP:
   WHILE LEFT_BRAC EXPRESSION RIGHT_BRAC BLOCK{
      printf("WHILE LOOP DETECTED\n");
   }
   ;

DO_WHILE_LOOP:
   DO BLOCK WHILE LEFT_BRAC EXPRESSION RIGHT_BRAC SEMICOLON{
      printf("DO WHILE LOOP DETECTED\n");
   }
   ;

/* SWITCH_CASE:
   SWITCH LEFT_BRAC EXPRESSION RIGHT_BRAC LEFT_CURL_BRAC case_lists RIGHT_CURL_BRAC{
      printf("SWITCH CASE STATEMENT DETECTED\n");
   }
   ;

case_lists:
   case_lists cases
   ;

cases:
   CASE IDENTIFIER COLON STMTS{
      printf("case %d detected.\n",$2);
   }
   ; */
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

