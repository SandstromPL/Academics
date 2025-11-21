%{
#include "y.tab.h"
#include "symbol.h"
#include <stdio.h>
#include <string.h> 
%}

%option noyywrap

%%
"if"        {return IF;}
"goto"      {return GOTO;}
"t"[0-9]* {yylval.str = strdup(yytext); return TEMP_VAR;}
[a-z][a-z0-9]* {yylval.str = strdup(yytext); return IDENTIFIER;} 
[0-9]+      {yylval.str = strdup(yytext); return CONSTANT;}
"L"[0-9]+   {yylval.str = strdup(yytext); return LABEL;}

"+"         {return PLUS;}
"-"         {return MINUS;}
"*"         {return MULTIPLY;}
"/"         {return DIVIDE;}
"<"         {return LT;}
">"         {return GT;}
"="         {return ASSGN;}
"!"         {return NEG;}
"=="        {return EQ;}
"!="        {return NE;}
"<="        {return LE;}
">="        {return GE;}

"["         {return LEFT_SQUARE;}
"]"         {return RIGHT_SQUARE;}
";"         {return SEMICOLON;}
":"         {return COLON;}

[ \t\n]+    { ;}
.           { printf("Unknown Character: %s\n", yytext); }
%%
