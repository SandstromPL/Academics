%{
#include "y.tab.h"
#include<string.h>
%}

%%
"for" 	    { return FOR_WORD; }
"int"       { return INT; }
"float"     { return FLOAT; }
"char"      { return CHAR; }
[a-zA-Z_][a-zA-Z0-9_]*    { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+ { yylval.str = strdup(yytext); return IDENTIFIER; }
";"         { return SEMICOLON; }
","         { return COMMA; }
"=" 	    { return EQUAL; }
"(" 	    { return LEFT_BRAC; }
")" 	    { return RIGHT_BRAC; }
[ \t\n]+    ;  // skip whitespace
.           { return yytext[0]; }
%%

int yywrap() {
    return 1;
}
