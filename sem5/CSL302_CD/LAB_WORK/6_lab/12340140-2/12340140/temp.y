%token INT DOUBLE BOOL STRING VOID MAIN ROUNDLBRACKET ROUNDRBRACKET SEMICOLON FOR BOOLEAN
%token IDENTIFIER MULTIPLITIVE ADDITIVE RELATIONAL EQUALITY AND OR ASSIGNMENT NEW CURLYRBRACKET  CURLYLBRACKET
%token CLASS INTEGER COMMA NEWARRAY UNARY RETURN BREAK IF ELSE DO WHILE SQUARERBRACKET DOT SQUARELBRACKET
%start compilation_unit

%left DOT SQUARELBRACKET SQUARERBRACKET

%left UNARY
%left MULTIPLITIVE
%left ADDITIVE
%left RELATIONAL
%left EQUALITY
%left AND
%left OR
%left ASSIGNMENT


%%

compilation_unit : main_function declarations_opt
        | declarations_plus main_function declarations_opt
        ;

declarations_opt: | declarations_opt declaration ;

declarations_plus: declaration | declarations_plus declaration;



declaration: variable_declaration | function_declaration | class_declaration  ;

main_function : VOID MAIN ROUNDLBRACKET ROUNDRBRACKET statement_block


variable_declaration:
       type_specifier IDENTIFIER SEMICOLON 
       |
       IDENTIFIER NEWARRAY ROUNDLBRACKET  INTEGER  COMMA type_specifier ROUNDRBRACKET SEMICOLON
       ;

function_declaration:
type_specifier IDENTIFIER ROUNDLBRACKET formal_params ROUNDRBRACKET statement_block 
;

class_declaration:
CLASS IDENTIFIER CURLYLBRACKET class_field_list CURLYRBRACKET
;

class_field_list:
    
    | 
    class_field_list class_field 
    ;

class_field: variable_declaration | function_declaration;
type_specifier : INT | DOUBLE | BOOL | STRING | VOID ;

formal_params:  | formal_param_list;

formal_param_list: formal_param | formal_param_list COMMA formal_param;

formal_param: type_specifier IDENTIFIER;

expression:
operator_expr
|
assignment_expr
|  
call_expr
|
new_expr
;

new_expr:
      NEW ROUNDLBRACKET IDENTIFIER ROUNDRBRACKET;

assignment_expr:
l_value ASSIGNMENT expression;

l_value:
      IDENTIFIER
      |
      expression DOT IDENTIFIER
      |
      expression SQUARELBRACKET expression SQUARERBRACKET
      ;
      
call_expr:
IDENTIFIER ROUNDLBRACKET actual_params ROUNDRBRACKET 
|
expression DOT IDENTIFIER ROUNDLBRACKET actual_params ROUNDRBRACKET 
;

actual_params: | actual_param_list;
actual_param_list : expression | actual_param_list COMMA expression;

operator_expr:
   or_expr
   |
   ROUNDLBRACKET operator_expr ROUNDRBRACKET
   ;
   
or_expr:
    and_expr
    | or_expr OR and_expr
    ;

and_expr:
    equality_expr
    | and_expr AND equality_expr
    ;

equality_expr:
    relational_expr
    | equality_expr EQUALITY relational_expr
    ;

relational_expr:
    additive_expr
    | relational_expr RELATIONAL additive_expr
    ;

additive_expr:
    multiplicative_expr
    | additive_expr ADDITIVE multiplicative_expr
    ;

multiplicative_expr:
    unary_expr
    | multiplicative_expr MULTIPLITIVE unary_expr
    ;

unary_expr:
    primary_operand
    | UNARY unary_expr
    ;
   
primary_operand: 
IDENTIFIER|
INTEGER
;




statement_block: CURLYLBRACKET statements CURLYRBRACKET;

statements :   statement statements |  variable_declaration statements | ;

statement : expression SEMICOLON |conditional_statement | loop_statement | other_statement| statement_block;


conditional_statement : IF ROUNDLBRACKET expression ROUNDRBRACKET statement | IF ROUNDLBRACKET expression ROUNDRBRACKET statement ELSE statement;

loop_statement : while_statement | for_statement | do_while_statement;

other_statement : return_statement | break_statement

while_statement: WHILE ROUNDLBRACKET expression ROUNDRBRACKET statement ;

do_while_statement: DO statement WHILE ROUNDLBRACKET expression ROUNDRBRACKET SEMICOLON ;

for_statement: FOR ROUNDLBRACKET expression SEMICOLON expression SEMICOLON expression ROUNDRBRACKET statement ;

break_statement:BREAK SEMICOLON ;

return_statement : RETURN expression SEMICOLON ;


%%