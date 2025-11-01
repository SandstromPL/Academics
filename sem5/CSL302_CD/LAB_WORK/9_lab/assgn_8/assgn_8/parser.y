%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symbol.h"

int yylex(void);
void yyerror(const char *s);

int temp_count = 1;
char* new_temp() {
    char *temp = (char*)malloc(5);
    sprintf(temp, "t%d", temp_count++);
    return temp;
}

char currentType[20];

int line_count = 1;
extern FILE* yyin;
extern int yylineno;
%}
%union {
    char* str;
}


%token INT FLOAT
%token FOR IF THEN ELSE ELIF SWITCH CASE DO WHILE
%token <str> ID
%token <str> NUM
%token EQUAL
%token AND OR NOT TRUE FALSE
%token SEMICOLON COMMA COLON
%token GE GT LE LT EEQ NEQ
%token LEFT_BRAC RIGHT_BRAC
%token LEFT_PAREN RIGHT_PAREN
%token ADD SUBTRACT MUL DIV REM

%type <str> expr

%right NOT
%left AND
%left OR

%start input

%%

input: stmts
       ;

stmts: stmt
       | stmts stmt
       ;

stmt: ID EQUAL expr SEMICOLON {
        int stmt_line = line_count++;
        printf("%d: %s = %s\n", stmt_line, $1, $3);
    }
    | declaration
    | FOR_LOOP SEMICOLON {
	printf("For loop initialized\n");
    }
    | IF_LOOP {
	printf("If statement initialized\n");
    }
    | IF_ELSE_LOOP {
	printf("If-else statement initialized\n");
    }
    | IF_ELSE_ELIF_LOOP {
	printf("If-else-elif statement initialized\n");
    }
    | SWITCH_LOOP SWITCH_BLOCK {
	printf("Switch loop initialized\n");
    }
    | WHILE_LOOP BLOCK {
	printf("While loop initialized\n");
    }
    | DO_WHILE_LOOP SEMICOLON {
	printf("Do while loop initialized\n");
    }
    | BLOCK;
    ;

BLOCK:
     LEFT_PAREN { enterScope(); } stmts RIGHT_PAREN { exitScope(); }
     ;

declaration:
        type id_list SEMICOLON
        ;

type:
        INT   { strcpy(currentType, "int"); }
      | FLOAT { strcpy(currentType, "float"); }
      ;

id_list:
        ID  { 
            addSymbol($1, currentType);
        }
        | id_list COMMA ID   { 
            addSymbol($3, currentType);
        }
        ;

expr: expr ADD expr {
		char *temp = new_temp();
        	printf("%d: %s = %s + %s\n", line_count++, temp, $1, $3);
        	$$ = temp;
      }
      | expr SUBTRACT expr {
		char *temp = new_temp();
        	printf("%d: %s = %s - %s\n", line_count++, temp, $1, $3);
        	$$ = temp;
      }
      | expr MUL expr {
		char *temp = new_temp();
        	printf("%d: %s = %s * %s\n", line_count++, temp, $1, $3);
        	$$ = temp;
      }
      | expr DIV expr {
		char *temp = new_temp();
        	printf("%d: %s = %s / %s\n", line_count++, temp, $1, $3);
        	$$ = temp;
      }
      | expr REM expr {
		char *temp = new_temp();
        	printf("%d: %s = %s %% %s\n", line_count++, temp, $1, $3);
        	$$ = temp;
      }
      | LEFT_BRAC expr RIGHT_BRAC {
		$$ = $2;
      }
      | expr GT expr {
    		char *temp = new_temp();
    		int if_line = line_count++;
    		int assign0_line = line_count++;
    		int goto_line = line_count++;
    		int assign1_line = line_count++;

    		printf("%d: if %s > %s goto %d\n", if_line, $1, $3, assign1_line);
    		printf("%d: %s = 0\n", assign0_line, temp);
    		printf("%d: goto %d\n", goto_line, assign1_line + 1);
    		printf("%d: %s = 1\n", assign1_line, temp);

    		$$ = temp;
      }
      | expr GE expr {
    		char *temp = new_temp();
    		int if_line = line_count++;
    		int assign0_line = line_count++;
    		int goto_line = line_count++;
    		int assign1_line = line_count++;

    		printf("%d: if %s >= %s goto %d\n", if_line, $1, $3, assign1_line);
    		printf("%d: %s = 0\n", assign0_line, temp);
    		printf("%d: goto %d\n", goto_line, assign1_line + 1);
    		printf("%d: %s = 1\n", assign1_line, temp);

    		$$ = temp;
      }
      | expr LT expr {
    		char *temp = new_temp();
    		int if_line = line_count++;
    		int assign0_line = line_count++;
    		int goto_line = line_count++;
    		int assign1_line = line_count++;

    		printf("%d: if %s < %s goto %d\n", if_line, $1, $3, assign1_line);
    		printf("%d: %s = 0\n", assign0_line, temp);
    		printf("%d: goto %d\n", goto_line, assign1_line + 1);
    		printf("%d: %s = 1\n", assign1_line, temp);

    		$$ = temp;
     }
     | expr LE expr {
    		char *temp = new_temp();
    		int if_line = line_count++;
    		int assign0_line = line_count++;
    		int goto_line = line_count++;
    		int assign1_line = line_count++;

    		printf("%d: if %s <= %s goto %d\n", if_line, $1, $3, assign1_line);
    		printf("%d: %s = 0\n", assign0_line, temp);
    		printf("%d: goto %d\n", goto_line, assign1_line + 1);
    		printf("%d: %s = 1\n", assign1_line, temp);

    		$$ = temp;
     }
     | expr EEQ expr {
    		char *temp = new_temp();
    		int if_line = line_count++;
    		int assign0_line = line_count++;
    		int goto_line = line_count++;
    		int assign1_line = line_count++;

    		printf("%d: if %s == %s goto %d\n", if_line, $1, $3, assign1_line);
    		printf("%d: %s = 0\n", assign0_line, temp);
    		printf("%d: goto %d\n", goto_line, assign1_line + 1);
    		printf("%d: %s = 1\n", assign1_line, temp);

    		$$ = temp;
     }
     | expr NEQ expr {
    		char *temp = new_temp();
    		int if_line = line_count++;
    		int assign0_line = line_count++;
    		int goto_line = line_count++;
    		int assign1_line = line_count++;

    		printf("%d: if %s != %s goto %d\n", if_line, $1, $3, assign1_line);
    		printf("%d: %s = 0\n", assign0_line, temp);
    		printf("%d: goto %d\n", goto_line, assign1_line + 1);
    		printf("%d: %s = 1\n", assign1_line, temp);

    		$$ = temp;
     }
     | expr AND expr {
    		char* temp = new_temp();
    		printf("%d: %s = %s && %s\n", line_count++, temp, $1, $3);
    		$$ = temp;
     }
     | expr OR expr {
    		char* temp = new_temp();
    		printf("%d: %s = %s || %s\n", line_count++, temp, $1, $3);
    		$$ = temp;
     }
     | NOT expr {
    		char* temp = new_temp();
    		printf("%d: %s = !%s\n", line_count++, temp, $2);
    		$$ = temp;
     }
     | TRUE {
    		$$ = strdup("true");
     }
     | FALSE {
    		$$ = strdup("false");
     }
     | ID {
    		$$ = $1;   
     }
     | NUM {
    		$$ = $1;   
     }
     ;

IF_LOOP:
    IF LEFT_BRAC expr RIGHT_BRAC THEN BLOCK
    ;

IF_ELSE_LOOP:
    IF_LOOP ELSE BLOCK
    ;

IF_ELSE_ELIF_LOOP:
    IF_LOOP ELIF LEFT_BRAC expr RIGHT_BRAC BLOCK ELSE BLOCK
    ;

FOR_LOOP:
    FOR LEFT_BRAC expr SEMICOLON expr SEMICOLON expr RIGHT_BRAC ID EQUAL expr SEMICOLON
    ;

SWITCH_LOOP:
     SWITCH LEFT_BRAC expr RIGHT_BRAC
     ;

WHILE_LOOP:
     WHILE LEFT_BRAC expr RIGHT_BRAC
     ;

DO_WHILE_LOOP:
     DO BLOCK WHILE LEFT_BRAC expr RIGHT_BRAC
     ;

SWITCH_BLOCK:
     LEFT_PAREN SWITCH_STATEMENTS RIGHT_PAREN
     ;

SWITCH_STATEMENTS:
     SWITCH_STATEMENTS SWITCH_STATEMENT
     | SWITCH_STATEMENT
     ;

SWITCH_STATEMENT:
     CASE NUM COLON stmts
     ;

%%

int main(int argc, char* argv[]) {
    if (argc == 2){
        FILE* fp = fopen(argv[1],"r");
        if (!fp) {
            perror(argv[1]);
            return 1;
        }
        yyin = fp;
    }else{
        printf("\nEnter Any Arithmetic Expression\n");
        printf("For eg:\n");
        printf("int a, b, c;\n");
        printf("float d, e, f;\n");
        printf("a = b * c - d / f;\n");
        printf("k = e or f >= g and h != i and not j;\n");
        printf("Now enter: ");
    }
    int result = yyparse();
    if (result == 0){
        printf("The above program is syntactically correct\n");
    }else{
        printf("The above program is syntactically not correct\n");
    }
    if (argc == 2){
        fclose(yyin);
    }
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}


