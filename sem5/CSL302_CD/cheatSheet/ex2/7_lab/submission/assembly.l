%{ 
	#include "y.tab.h"
	#include<string.h> 
%}

%% 
"MOV" { return MOV; }
"ADD" { return ADD; }
"SUB" { return SUB; }
"MUL" { return MUL; }
"DIV" { return DIV; }
"LOAD" { return LOAD; }
"STORE" { return STORE; }
"JMP" { return JMP; }
"CMP" { return CMP; }
"HALT" { return HALT; }

[A-Z]+ {yylval.str = strdup(yytext); return LABEL;}
R[0-9]+ {yylval.str = strdup(yytext); return REGISTER;}
#[-]?[0-9]+ {yylval.str = strdup(yytext); return IMMEDIATE_NUMBER;}

\;.* {/*ignore comments*/}
"," {return COMMA;} 
";" {return SEMI_COLON;}
":" {return COLON;} 
[ \t\n]+ {/*whitespace*/}
. { return yytext[0]; } 
%% 

int yywrap() { 
	return 1; 
}
