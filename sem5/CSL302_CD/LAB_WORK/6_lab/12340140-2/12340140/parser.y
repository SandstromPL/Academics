%token INT DOUBLE BOOL STRING VOID CLASS IF ELSE WHILE FOR DO BREAK RETURN
%token NEWARRAY NEW MAIN
%token ASSIGN EQ NEQ LT LE GT GE AND OR NOT
%token PLUS MINUS MUL DIV MOD
%token L_RND_BRC R_RND_BRC L_CURL_BRC R_CURL_BRC L_SQR_BRC R_SQR_BRC SEMICOLON COMMA DOT
%token IDENTIFIER HEXA_CONST INT_CONST DOUBLE_CONST STR_CONST TRUE_CONST FALSE_CONST

%start program_start

%right ASSIGN
%left OR
%left AND
%left EQ NEQ
%left LT LE GT GE
%left PLUS MINUS
%left MUL DIV MOD
%right NOT UMINUS
%nonassoc IFX
%nonassoc ELSE

%%

program_start: decl_list;

decl_list: decl | decl_list decl;

decl: var_decl | func_decl | class_decl;

var_decl: type_specifier IDENTIFIER SEMICOLON
        | IDENTIFIER NEWARRAY L_RND_BRC expr COMMA type_specifier R_RND_BRC SEMICOLON
        ;

type_specifier: INT | DOUBLE | BOOL | STRING | VOID;

func_decl: type_specifier IDENTIFIER L_RND_BRC formals R_RND_BRC stmt_block
         | VOID MAIN L_RND_BRC R_RND_BRC stmt_block
         ;

formals: /* empty */ | formal_list;

formal_list: formal | formal_list COMMA formal;

formal: type_specifier IDENTIFIER;

class_decl: CLASS IDENTIFIER L_CURL_BRC field_list R_CURL_BRC;

field_list: /* empty */ | field_list field;

field: var_decl | func_decl;

stmt_block: L_CURL_BRC var_decl_list stmt_list R_CURL_BRC;

var_decl_list: /* empty */ | var_decl_list var_decl;
stmt_list: /* empty */ | stmt_list stmt;

stmt: opt_expr SEMICOLON
    | if_stmt
    | while_stmt
    | do_while_stmt
    | for_stmt
    | break_stmt
    | return_stmt
    | stmt_block
    ;

opt_expr: /* empty */ | expr;

if_stmt: IF L_RND_BRC expr R_RND_BRC stmt %prec IFX
       | IF L_RND_BRC expr R_RND_BRC stmt ELSE stmt
       ;

while_stmt: WHILE L_RND_BRC expr R_RND_BRC stmt;

do_while_stmt: DO stmt WHILE L_RND_BRC expr R_RND_BRC SEMICOLON;

for_stmt: FOR L_RND_BRC opt_expr SEMICOLON opt_expr SEMICOLON opt_expr R_RND_BRC stmt;

return_stmt: RETURN opt_expr SEMICOLON;

break_stmt: BREAK SEMICOLON;

expr: postfix_expr ASSIGN expr
    | expr OR expr
    | expr AND expr
    | expr EQ expr
    | expr NEQ expr
    | expr LT expr
    | expr LE expr
    | expr GT expr
    | expr GE expr
    | expr PLUS expr
    | expr MINUS expr
    | expr MUL expr
    | expr DIV expr
    | expr MOD expr
    | MINUS expr %prec UMINUS
    | NOT expr
    | postfix_expr
    ;

postfix_expr: primary_expr
            | postfix_expr L_SQR_BRC expr R_SQR_BRC
            | postfix_expr DOT IDENTIFIER
            | postfix_expr L_RND_BRC actuals R_RND_BRC
            ;

primary_expr: IDENTIFIER
            | constant
            | L_RND_BRC expr R_RND_BRC
            | NEW L_RND_BRC IDENTIFIER R_RND_BRC
            ;

actuals: /* empty */ | expr_list;

expr_list: expr | expr_list COMMA expr;

constant: INT_CONST
        | HEXA_CONST
        | DOUBLE_CONST
        | STR_CONST
        | TRUE_CONST
        | FALSE_CONST
        ;

%%
