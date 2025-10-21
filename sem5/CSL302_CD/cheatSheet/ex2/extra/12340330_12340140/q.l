%{
#include "y.tab.h"
#include <stdio.h>
#include <string.h> 
extern FILE *yyin;
%}

%option noyywrap yylineno

%%
\/\/[^\n]*                       { ; }
\/\*([^*]|\*+[^/])*\*+\/         { ; }
(extends|implements|ReadInteger|ReadLine|interface|null|this|Print) {yylval.str = strdup(yytext); return KEYWORD;}
"if" {return IF; }
"else" {return ELSE; }
"while" {return WHILE; }
"do" {return DO; }
"for" {return FOR; }
"return" {return RETURN;}
"break" {return BREAK;}
"New" {return NEW;}
"NewArray" {return NEW_ARRAY;}
"class" {return CLASS;}
(true|false) {yylval.str = strdup(yytext); return BOOLEAN;}
"void"|"int"|"double"|"bool"|"string" {yylval.str = strdup(yytext); return TYPE;}
"." {return DOT;}
"+" {return ADD;}
"-" {return SUBTRACT;}
"*" {return MULTIPLY;}
"/" {return DIVIDE;}
"%" {return REM;}
"=" {return ASSGN;}
"!" {return NEG;}
"<" {return LT;}
">" {return GT;}
"==" {return EQ;}
"!=" {return NE;}
"<=" {return LE;}
">=" {return GE;}
"&&" {return AND; }
"||" {return OR;}
"(" {return LEFT_BRAC; }
")" {return RIGHT_BRAC; }
"{" {return LEFT_PAREN; }
"}" {return RIGHT_PAREN; }
"[" {return LEFT_SQUARE;}
"]" {return RIGHT_SQUARE;}
";" {return SEMICOLON;}
":" {return COLON;}
"," {return COMMA;}
[a-zA-Z][a-zA-Z0-9_]{0,30} {yylval.str = strdup(yytext); return IDENTIFIER;}
-?[0-9]+\.[0-9]*([eE][+-]?[0-9]+)? {yylval.str = strdup(yytext); return DOUBLE; }
-?([0-9]+|0(x|X)[0-9a-fA-F]+) {yylval.str = strdup(yytext); return INTEGER;}
\"([^"\\\n]|\\.)*\"   { yylval.str = strdup(yytext); return STRING; }
[ \t\n]+ { ;}
%%