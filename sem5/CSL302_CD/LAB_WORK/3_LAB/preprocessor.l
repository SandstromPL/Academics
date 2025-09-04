%{
#include <stdio.h>
%}

%%
"#define"          { printf("%s DEFINE\n", yytext); }
"#include"         { printf("%s INCLUDE\n", yytext); }
"#ifdef"           { printf("%s IFDEF\n", yytext); }
"#ifndef"          { printf("%s IFNDEF\n", yytext); }
"#if"              { printf("%s IF\n", yytext); }
"#else"            { printf("%s ELSE\n", yytext); }
"#elif"            { printf("%s ELIF\n", yytext); }
"#endif"           { printf("%s ENDIF\n", yytext); }
"#undef"           { printf("%s UNDEF\n", yytext); }
"#pragma"          { printf("%s PRAGMA\n", yytext); }
"#error"           { printf("%s ERROR\n", yytext); }
"#line"            { printf("%s LINE\n", yytext); }

\"[^\"]*\"         { printf("%s STRING_LITERAL\n", yytext); }
[a-zA-Z]+\.h       { printf("%s FILENAME\n", yytext); }
[a-zA-Z]+\.c       { printf("%s FILENAME\n", yytext); }

0x[0-9A-Fa-f]+     { printf("%s INTEGER\n", yytext); }
[0-9]+             { printf("%s INTEGER\n", yytext); }
[0-9]+\.[0-9]+     { printf("%s FLOAT\n", yytext); }

\+                 { printf("%s PLUS\n", yytext); }
\-                 { printf("%s MINUS\n", yytext); }
\*                 { printf("%s MUL\n", yytext); }
\/                 { printf("%s DIV\n", yytext); }
"=="               { printf("%s EQEQ\n", yytext); }

"@@"[^\n]*         { printf("%s COMMENT\n", yytext); }

\$[A-Z][A-Za-z0-9]*  { printf("%s IDENTIFIER\n", yytext); }

[ \t\n]+           ;
.                  { printf("%s\n", yytext); }
%%

int yywrap(){
    return 1;
}

int main() {
    yylex();
    return 0;
}
