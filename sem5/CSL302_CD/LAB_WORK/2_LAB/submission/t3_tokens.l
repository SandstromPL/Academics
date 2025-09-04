/*Definition*/

%{
    #include<stdio.h>
%}

/*Rules*/

%%

[A-Z]([a-z])*([ \t]*)([A-Z]([a-z])*) {printf("%s\tNAME\n",yytext);}
([0-9]{3}){2}("-")([0-9]{4}) {printf("%s\tPHONE_NUMBER\n",yytext);}
[a-zA-Z]([a-zA-Z0-9]+)("@")([a-z]+)(".")([a-z]+)(".")([a-z]*) {printf("%s\tEMAIL\n",yytext);}
[0-9]{4}([ \t]*([0-9]{4})){3} {printf("%s\tCREDIT_CARD\n",yytext);}
(([0|1|2]+[0-9]+|[3][0|1])("-"))([0|1]+[0-9]+)("-")([0-9]{2}|[0-9]{4}) {printf("%s\tDOB\n",yytext);}

.|\n;

%%

/*yywrap function*/
int yywrap()
{
    return 1;
}

/*Auxiliary Function*/
int main(void){

    printf("Enter the string\n");
    yylex();
    return 0;
}
