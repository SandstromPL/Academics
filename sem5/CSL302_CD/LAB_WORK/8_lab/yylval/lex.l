%{
#include "y.tab.h"
%}
%option noyywrap

%%
[0-9]+\.[0-9]+     { yylval.fval = atof(yytext); return FLOAT; }
[0-9]+             { yylval.ival = atoi(yytext); return INT; }
[a-zA-Z_][a-zA-Z0-9_]* { yylval.sval = strdup(yytext); return ID; }
[+\-*/=;]          { return yytext[0]; }
[ \t\n]            ;
.                  { return yytext[0]; }
%%
