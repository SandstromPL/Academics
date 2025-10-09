%option noyywrap
%x COMMENT
%{
#include <stdio.h>
%}

%%
"MOV"     { printf("TOKEN_MOV\n"); }
"ADD"    { printf("TOKEN_ADD\n"); }
"SUB"      { printf("TOKEN_SUB\n"); }
"#MUL"     { printf("TOKEN_MUL\n"); }
"#DIV"         { printf("TOKEN_DIV\n"); }
"#LOAD"       { printf("TOKEN_LOAD\n"); }
"#STORE"       { printf("TOKEN_STORE\n"); }
"#JMP"      { printf("TOKEN_JMP\n"); }
"#CMP"      { printf("TOKEN_CMP\n"); }
"#HALT"     { printf("TOKEN_HALT\n"); }

[A-Z]+          {printf("TOKEN_LABEL: %s\n", yytext);}
R[0-9]+         {printf("TOKEN_REGISTER: %s\n", yytext);}
#[-]?[0-9]+     {printf("TOKEN_IMMEDIATE_NUMBER: %s\n", yytext);}
\;.*         
[\,\;\:]        {printf("TOKEN_DELIMITER: %s\n", yytext);}
[ \t\n]+        
.               { printf("UNRECOGNIZED: %s\n", yytext); }
%%

int main() {
    yylex();
    return 0;
}
