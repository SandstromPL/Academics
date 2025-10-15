program : FuncMain declarations
        | declarations_plus FuncMain declarations
        ;

declarations: | declarations declaration ;

declarations_plus: declaration | declarations_plus declaration;




declaration: VarDecl | FuncDecl | ClassDecl  ;

FuncMain : VOID MAIN ROUNDLBRACKET ROUNDRBRACKET StmtBlock
	

VarDecl:
       type IDENTIFIER SEMICOLON 
       |
       IDENTIFIER NEWARRAY ROUNDLBRACKET  INTEGER  COMMA type ROUNDRBRACKET SEMICOLON
       ;

FuncDecl:
	type IDENTIFIER ROUNDLBRACKET formalParameters ROUNDRBRACKET StmtBlock 
	;
	
ClassDecl:
	CLASS IDENTIFIER CURLYLBRACKET FieldList CURLYRBRACKET
	;

FieldList:
    
    | 
    FieldList field 
    ;
	
field: VarDecl | FuncDecl;
type : INT | DOUBLE | BOOL | STRING | VOID ;

formalParameters:  | formalParameterList;

formalParameterList: formalParameter | formalParameterList COMMA formalParameter;

formalParameter: type IDENTIFIER;

Expression:
	OperatorExp
	|
	AssignExp
	|  
	CallExp
	|
	NewExp
	;
	
NewExp:
      NEW ROUNDLBRACKET IDENTIFIER ROUNDRBRACKET;

AssignExp:
	Lvalue ASSIGNMENT Expression;
	
Lvalue:
      IDENTIFIER
      |
      Expression DOT IDENTIFIER
      |
      Expression SQUARELBRACKET Expression SQUARERBRACKET
      ;
      
CallExp:
	IDENTIFIER ROUNDLBRACKET ActualParameters ROUNDRBRACKET 
	|
	Expression DOT IDENTIFIER ROUNDLBRACKET ActualParameters ROUNDRBRACKET 
	;

ActualParameters: | ActualParametersList;
ActualParametersList : Expression | ActualParametersList COMMA Expression;

OperatorExp:
	   OrExp
	   |
	   ROUNDLBRACKET OperatorExp ROUNDRBRACKET
	   ;
	   
OrExp:
    AndExp
    | OrExp OR AndExp
    ;

AndExp:
    EqualityExp
    | AndExp AND EqualityExp
    ;

EqualityExp:
    RelationalExp
    | EqualityExp EQUALITY RelationalExp
    ;

RelationalExp:
    AdditiveExp
    | RelationalExp RELATIONAL AdditiveExp
    ;

AdditiveExp:
    MultiplicativeExp
    | AdditiveExp ADDITIVE MultiplicativeExp
    ;

MultiplicativeExp:
    UnaryExp
    | MultiplicativeExp MULTIPLITIVE UnaryExp
    ;

UnaryExp:
    Operand
    | UNARY UnaryExp
    ;
	   
Operand: 
	IDENTIFIER|
	INTEGER
	;
	



StmtBlock: CURLYLBRACKET Stmts CURLYRBRACKET;

Stmts :   Statement Stmts |  VarDecl Stmts | ;

Statement : Expression SEMICOLON |ConditionalStmt | LoopStmt | OtherStmt| StmtBlock;


ConditionalStmt : IF ROUNDLBRACKET Expression ROUNDRBRACKET Statement | IF ROUNDLBRACKET Expression ROUNDRBRACKET Statement ELSE Statement;

LoopStmt : WhileStmt | ForStmt | DoWhileStmt;

OtherStmt : ReturnStmt | BreakStmt

WhileStmt: WHILE ROUNDLBRACKET Expression ROUNDRBRACKET Statement ;

DoWhileStmt: DO Statement WHILE ROUNDLBRACKET Expression ROUNDRBRACKET SEMICOLON ;

ForStmt: FOR ROUNDLBRACKET Expression SEMICOLON Expression SEMICOLON Expression ROUNDRBRACKET Statement ;

BreakStmt:BREAK SEMICOLON ;

ReturnStmt : RETURN Expression SEMICOLON ;


%%
