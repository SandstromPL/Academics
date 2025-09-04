%{
	#include<stdio.h>
%}

%%

[/](([a-zA-Z0-9]+|"..")[/])*([a-zA-Z0-9]+\.(txt|dat))? {printf("The PATH : %s is VALID\n",yytext);}
.+	{printf("INVALID PATH\n");}

%%

int yywrap(){
	return 1;
}

int main(){
	printf("Enter the path :\n");
	yylex();
	return 0;
}
