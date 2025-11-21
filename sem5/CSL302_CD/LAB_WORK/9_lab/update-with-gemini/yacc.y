%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symbol.h" /* Using your old symbol.h */

int temp_count = 1;
int label_count = 1;
int current_scope = 0; /* Simple counter for scope */
char* current_type;

void yyerror(const char *s);
int yylex(void);

/* Helper for t1, t2... */
char* new_temp() {
    char *temp = (char*)malloc(10);
    sprintf(temp, "t%d", temp_count++);
    return temp;
}

/* Helper for L1, L2... */
char* new_label() {
    char *lbl = (char*)malloc(10);
    sprintf(lbl, "L%d", label_count++);
    return lbl;
}

%}

%union {
    char *str;
}

%token <str> ID NUM
%token ASSIGN PLUS MINUS MULTIPY DIVIDE 
%token LBRAC RBRAC LCURL RCURL
%token LT GT LE GE NE EQ
%token AND OR NOT TRUE FALSE 
%token IF ELSE WHILE
%token INT FLOAT COMMA SEMICOLON

/* Precedence to handle if-else ambiguity */
%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%left OR
%left AND
%left EQ NE
%left LT GT LE GE
%left PLUS MINUS
%left MULTIPY DIVIDE
%right NOT

%type <str> expr

%%

program : stmts
        ;

stmts   : stmts stmt
        | /* empty */
        ;

stmt    : declaration
        | assignment
        | if_stmt
        | while_stmt
        | block_stmt
        ;

/* Block handling: Increment scope on {, decrement on } */
block_stmt: LCURL { current_scope++; } stmts RCURL { current_scope--; }
          ;

/* --- IF-ELSE Logic --- */
if_stmt : IF LBRAC expr RBRAC 
          {
              char* l_false = new_label();
              printf("ifFalse %s goto %s\n", $3, l_false);
              $<str>$ = l_false; /* Store label for later */
          }
          stmt 
          {
               char* l_next = new_label();
               printf("goto %s\n", l_next);
               printf("%s:\n", $<str>5); /* Print False Label */
               $<str>$ = l_next;
          }
          else_part
          ;

else_part : /* empty */ %prec LOWER_THAN_ELSE
            {
                printf("%s:\n", $<str>0); /* Print Next Label */
            }
          | ELSE stmt
            {
                printf("%s:\n", $<str>0); /* Print Next Label */
            }
          ;

/* --- WHILE Logic --- */
while_stmt : WHILE 
             {
                 char* l_start = new_label();
                 printf("%s:\n", l_start);
                 $<str>$ = l_start;
             }
             LBRAC expr RBRAC 
             {
                 char* l_end = new_label();
                 printf("ifFalse %s goto %s\n", $4, l_end);
                 $<str>$ = l_end;
             }
             stmt
             {
                 printf("goto %s\n", $<str>2); /* Jump to start */
                 printf("%s:\n", $<str>6);     /* Label for end */
             }
           ;

/* --- Assignments & Declarations --- */
assignment: ID ASSIGN expr SEMICOLON {
        printf("%s = %s\n", $1, $3);
    }
    ;

declaration : type id_list SEMICOLON
            ;

type        : INT   { current_type = "int"; }
            | FLOAT { current_type = "float"; }
            ;

/* Using YOUR insertSymbol function */
id_list     : ID { insertSymbol($1, current_type, current_scope); } 
            | id_list COMMA ID { insertSymbol($3, current_type, current_scope); }
            ;

/* --- Expressions (Short Circuit) --- */
expr: expr PLUS expr { $$ = new_temp(); printf("%s = %s + %s\n", $$, $1, $3); }
    | expr MINUS expr { $$ = new_temp(); printf("%s = %s - %s\n", $$, $1, $3); }
    | expr MULTIPY expr { $$ = new_temp(); printf("%s = %s * %s\n", $$, $1, $3); }
    | expr DIVIDE expr { $$ = new_temp(); printf("%s = %s / %s\n", $$, $1, $3); }
    | expr LT expr { $$ = new_temp(); printf("%s = %s < %s\n", $$, $1, $3); }
    | expr GT expr { $$ = new_temp(); printf("%s = %s > %s\n", $$, $1, $3); }
    | expr LE expr { $$ = new_temp(); printf("%s = %s <= %s\n", $$, $1, $3); }
    | expr GE expr { $$ = new_temp(); printf("%s = %s >= %s\n", $$, $1, $3); }
    | expr EQ expr { $$ = new_temp(); printf("%s = %s == %s\n", $$, $1, $3); }
    | expr NE expr { $$ = new_temp(); printf("%s = %s != %s\n", $$, $1, $3); }
    
    /* Short Circuit AND */
    | expr AND expr {
        $$ = new_temp();
        char* l_true = new_label();
        char* l_end = new_label();
        printf("ifFalse %s goto %s\n", $1, l_true); // Check 1st
        printf("ifFalse %s goto %s\n", $3, l_true); // Check 2nd
        printf("%s = true\n", $$);
        printf("goto %s\n", l_end);
        printf("%s:\n", l_true);
        printf("%s = false\n", $$);
        printf("%s:\n", l_end);
    }
    /* Short Circuit OR */
    | expr OR expr {
        $$ = new_temp();
        char* l_true = new_label();
        char* l_end = new_label();
        printf("if %s goto %s\n", $1, l_true);
        printf("if %s goto %s\n", $3, l_true);
        printf("%s = false\n", $$);
        printf("goto %s\n", l_end);
        printf("%s:\n", l_true);
        printf("%s = true\n", $$);
        printf("%s:\n", l_end);
    }
    | NOT expr { $$ = new_temp(); printf("%s = not %s\n", $$, $2); }
    | TRUE { $$ = "true"; }
    | FALSE { $$ = "false"; }
    | LBRAC expr RBRAC { $$ = $2; }
    | ID { $$ = $1; }
    | NUM { $$ = $1; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Enter program:\n");
    yyparse();
    return 0;
}
