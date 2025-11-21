%{
    #include "y.tab.h"
    #include <stdlib.h>
    #include <string.h>
%}

%%
"int"   {return INT;}
"float" {return FLOAT;}
"if"    {return IF;}
"else"  {return ELSE;}
"while" {return WHILE;}
"true"  {return TRUE;}
"false" {return FALSE;}
"not"   {return NOT;}
"and"   {return AND;}
"or"    {return OR;}

[0-9]+  { yylval.str = strdup(yytext); return NUM; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.str = strdup(yytext); return ID;}

"+" {return PLUS;}
"-" {return MINUS;}
"*" {return MULTIPY;}
"/" {return DIVIDE;}
"=" {return ASSIGN;}
"(" {return LBRAC;}
")" {return RBRAC;}
"{" {return LCURL;}
"}" {return RCURL;}
"<" {return LT;}
">" {return GT;}
">=" {return GE;}
"<=" {return LE;}
"==" {return EQ;}
"!=" {return NE;}
"," {return COMMA;}
";" {return SEMICOLON;}

[ \t\n\r]+ {;} /* Ignore whitespace and Windows CR */
.          {return yytext[0];}
%%

int yywrap() {
    return 1;
}
