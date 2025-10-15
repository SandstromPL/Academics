%{
#include "y.tab.h"
#include<string.h>
%}

%%
"if"        {return IF;}
"then"      {return THEN;}
"else"      {return ELSE;}
"elseif"    {return ELIF;}
"while"     {return WHILE;}
"do"        {return DO;}
"switch"    {return SWTICH;}
"case"      {return CASE;}
"for" 	   { return FOR_WORD; }
"int"       { return INT; }
"float"     { return FLOAT; }
"char"      { return CHAR; }
[a-zA-Z_][a-zA-Z0-9_]*    { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+ { yylval.str = strdup(yytext); return IDENTIFIER; }
":"         {return COLON;}
";"         { return SEMICOLON; }
","         { return COMMA; }
"=" 	    { return EQUAL; }
"(" 	    { return LEFT_BRAC; }
")" 	    { return RIGHT_BRAC; }
"{"       { return LEFT_CURL_BRAC; }
"}"       { return RIGHT_CURL_BRAC; }
"<="        {return LES_EQUAL;}
">="        {return GRT_EQUAL;}
"!="        {return NOT_EQUAL;}
">"         {return GRT;}
"<"         {return LES;}
[ \t\n]+    ;  // skip whitespace
.           { return yytext[0]; }
%%

int yywrap() {
    return 1;
}
