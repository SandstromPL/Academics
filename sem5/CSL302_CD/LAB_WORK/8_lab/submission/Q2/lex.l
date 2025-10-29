%{
	#include "y.tab.h"
	#include <stdlib.h>
	#include <string.h>
%}

%%
[0-9]+                  { yylval.str = strdup(yytext);
                          return NUM; }
"and"	{return AND;}
"or"	{return OR;}
"not"	{return NOT;}
"true"	{return TRUE;}
"false"	{return FALSE;}
"int"   {return INT;}
"float" {return FLOAT;}
[a-zA-Z][a-zA-Z0-9]* { yylval.str = strdup(yytext); return ID;
                        }
"+" {return PLUS;}
"-" {return MINUS;}
"*" {return MULTIPY;}
"/" {return DIVIDE;}
"=" {return ASSIGN;}
"(" {return LBRAC;}
")" {return RBRAC;}
"<" {return LT;}
">" {return GT;}
">=" {return GE;}
"<=" {return LE;}
"==" {return EQ;}
"!=" {return NE;}
"," {return COMMA;}
";" {return SEMICOLON;}
[ \t\n]+ {;}            
. {return yytext[0];}
%%

int yywrap() {
    return 1;
}