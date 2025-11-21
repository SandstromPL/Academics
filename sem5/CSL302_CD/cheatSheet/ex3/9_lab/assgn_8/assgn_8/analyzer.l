%{
#include "y.tab.h"
#include <stdlib.h>
#include <string.h>
extern FILE *yyin;
%}

%option noyywrap yylineno

%%
"int"       { return INT; }
"float"     { return FLOAT; }
"for" 	    { return FOR; }
"if"	    { return IF; }
"then"	    { return THEN; }
"else"	    { return ELSE; }
"elif"      { return ELIF; }
"SWITCH"    { return SWITCH; }
"CASE"      { return CASE; }
"while"     { return WHILE; }
"do"        { return DO; }
"and"       { return AND; }
"or"        { return OR; }
"not"       { return NOT; }
"true"      { return TRUE; }
"false"     { return FALSE; }
";"         { return SEMICOLON; } 
":"	    { return COLON; }
","         { return COMMA; }
"=="	    { return EEQ; } 
">="	    { return GE; } 
"<="	    { return LE; } 
"!="	    { return NEQ; } 
">" 	    { return GT; } 
"<"	        { return LT; } 
"=" 	    { return EQUAL; }
"(" 	    { return LEFT_BRAC; }
")"	    { return RIGHT_BRAC; }
"{"	    { return LEFT_PAREN; }
"}"	    { return RIGHT_PAREN; }
"+" 	    { return ADD; }
"-"	    { return SUBTRACT; }
"*"	    { return MUL; }
"/"	    { return DIV; }
"%"	    { return REM; }
[a-zA-Z_][a-zA-Z0-9_]*    { yylval.str = strdup(yytext); return ID; }
[0-9]+ { yylval.str = strdup(yytext); return NUM; }
[ \t] ;
[\n]  ; 
%%

