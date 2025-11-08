%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symbol.h"

int temp_count = 1;
int label_count = 1;
char* current_type;

char* new_temp() {
    char *temp = (char*)malloc(12);
    sprintf(temp, "t%d", temp_count++);
    return temp;
}

char* new_label() {
    char *label = (char*)malloc(5);
    sprintf(label, "L%d", label_count++);
    return label;
}

void yyerror(const char *s);
int yylex(void);

%}

%union {
    char *str;

    struct{
        char * truelabel;
        char * falselabel;
    }labels;
}

%token <str> ID
%token <str> NUM
%token ASSIGN PLUS MINUS MULTIPY DIVIDE LBRAC RBRAC LCURL RCURL
%token LT GT LE GE NE EQ
%token AND OR NOT TRUE FALSE IF ELSE THEN WHILE
%token INT FLOAT COMMA SEMICOLON

%type <str> expr
%type <labels> b_expr

%start program
%right ASSIGN
%left PLUS MINUS
%left MULTIPY DIVIDE
%nonassoc LT GT LE GE NE EQ
%nonassoc dangling
%nonassoc ELSE
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
        | if_stmt
        | while_stmt
        | LCURL stmts RCURL
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


b_expr: expr LT expr {
          $$.truelabel = new_label();
          $$.falselabel = new_label();

          printf("if %s < %s goto %s\n", $1, $3, $$.truelabel);
          printf("goto %s\n", $$.falselabel);
      }
    |   expr GT expr {
          $$.truelabel = new_label();
          $$.falselabel = new_label();

          printf("if %s > %s goto %s\n", $1, $3, $$.truelabel);
          printf("goto %s\n", $$.falselabel);
      }
    |   expr LE expr {
          $$.truelabel = new_label();
          $$.falselabel = new_label();

          printf("if %s <= %s goto %s\n", $1, $3, $$.truelabel);
          printf("goto %s\n", $$.falselabel);
      }
    |   expr GE expr {
          $$.truelabel = new_label();
          $$.falselabel = new_label();

          printf("if %s >= %s goto %s\n", $1, $3, $$.truelabel);
          printf("goto %s\n", $$.falselabel);
      }
    |   expr EQ expr {
          $$.truelabel = new_label();
          $$.falselabel = new_label();

          printf("if %s == %s goto %s\n", $1, $3, $$.truelabel);
          printf("goto %s\n", $$.falselabel);
      }
    |   expr NE expr {
          $$.truelabel = new_label();
          $$.falselabel = new_label();

          printf("if %s != %s goto %s\n", $1, $3, $$.truelabel);
          printf("goto %s\n", $$.falselabel);
      }
    |   b_expr AND {<str> $$ = new_label(); printf("%s:\n", $$); } b_expr {
          printf("/* Backpatch %s to %s */\n", $1.truelabel, $3); 
          $$.truelabel = $4.truelabel;
          printf("/* Merge %s and %s into falselist */\n", $1.falselabel, $4.falselabel);
          $$.falselabel = $1.falselabel;
      }
    | b_expr OR {<str> $$ = new_label(); printf("%s:\n", $$); } b_expr {
          printf("/* Backpatch %s to %s */\n", $1.falselabel, $3);
          printf("/* Merge %s and %s into truelist */\n", $1.truelabel, $4.truelabel);
          $$.truelabel = $1.truelabel;
          $$.falselabel = $4.falselabel;
      }
    | NOT b_expr {
          $$.truelabel = $2.falselabel;
          $$.falselabel = $2.truelabel;
      }
    | LBRAC b_expr RBRAC {
          $$ = $2;
      }
    ;

if_stmt: IF LBRAC b_expr RBRAC THEN {<str> $$ = new_label(); printf("%s:\n", $$); } stmt %prec dangling{

             printf("/* Backpatch %s to %s */\n", $3.truelabel, $6);
             
             printf("%s:\n", $3.falselabel);
         }
       |
       IF LBRAC b_expr RBRAC THEN {<str> $$ = new_label(); printf("%s:\n", $$); } stmt {<str> $$ = new_label(); printf("goto %s\n", $$); } ELSE {<str> $$ = new_label(); printf("%s:\n", $$); } stmt %prec ELSE{
                  
                  printf("/* Backpatch %s to %s */\n", $3.truelabel, $6);

                  printf("/* Backpatch %s to %s */\n", $3.falselabel, $10);

                  printf("%s:\n", $8);
              }
       ;


while_stmt: WHILE {<str> $$ = new_label(); printf("%s:\n", $$); } LBRAC b_expr RBRAC {<str> $$ = new_label(); printf("%s:\n", $$); } stmt {
                printf("/* Backpatch %s to %s */\n", $4.truelabel, $6);

                printf("goto %s\n", $2);
                
                printf("%s:\n", $4.falselabel);
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