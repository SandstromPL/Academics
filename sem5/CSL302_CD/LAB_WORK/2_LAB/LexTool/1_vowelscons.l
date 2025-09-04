%{
	#include<stdio.h>
	int vowel=0;
	int cons=0;
%}
%%
"a"|"e"|"i"|"o"|"u"|"A"|"E"|"I"|"O"|"U" {printf("%s Vowel\n", yytext);}
[a-zA-z] {printf("%s Cons\n", yytext);}

%%
int yywrap() {return 1;}
int main()
{
	printf("Enter String\n");
	yylex();
	return 0;
}

