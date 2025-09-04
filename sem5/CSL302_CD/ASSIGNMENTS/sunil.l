%{
#include <stdio.h>
%}

%%

"void"|"int"|"double"|"bool"|"string"|"extends"|"implements"|\
"for"|"while"|"ReadInteger"|"ReadLine"|"class"|"interface"|\
"if"|"else"|"return"|"null"|"this"|"break"|"New"|"NewArray"|"Print"\
    { printf("Keyword : %s\n", yytext); }

[a-zA-Z][a-zA-Z0-9_]{0,30} 
    { printf("Identifier : %s\n", yytext); }

[ \t\n]+ 
    { /* ignore whitespace */ }

"true"{ printf("Constant : %s\n", yytext); }

. 
    { printf("Invalid Token : %s\n", yytext); }

%%

int main(void) {
    yylex();
    return 0;
}

/* 
Note:
1. Keywords: void int double bool string extends implements ...
2. Identifiers: sequence of letters, digits, underscores, starting with letter
3. Whitespace: ignored, only separates tokens
4. Constants: integers handled
*/
