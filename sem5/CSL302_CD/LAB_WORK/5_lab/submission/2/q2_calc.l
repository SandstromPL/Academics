%{ 
   /* Definition section */
  #include<stdio.h> 
  #include "y.tab.h" 
  extern YYSTYPE yylval; 
%} 
  
/* Rule Section */
%% 
"for"       { return FOR; }
[a-zA-Z_][a-zA-Z0-9_]* { 
          yylval.index = yytext[0];
          return IDENTIFIER;
       }
[0-9]+ { 
          yylval.val=atoi(yytext); 
          return NUMBER; 
       } 
";"         { return SEMICOLON; }
[\t] ; 
  
[\n] return '\n'; 
  
. return yytext[0]; 
  
%% 
  
int yywrap() 
{ 
 return 1; 
}
