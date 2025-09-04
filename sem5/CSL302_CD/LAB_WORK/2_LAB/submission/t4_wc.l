%{
    #include<stdio.h>
    #include<string.h>
    extern FILE *yyin;
    int line_count = 0;
    int word_count = 0;
    int char_count = 0;    
%}

/*RULES*/
%%
\n          {line_count++; char_count++;}
[ \t]+      {char_count += yyleng;}
[^ \t\n]+   {word_count++; char_count += yyleng;}
.           {char_count++;}
%%

int yywrap(){
    return 1;
}

int main(int argc,char * argv[]){
    if(argc < 2){
        fprintf(stderr,"Usage: %s <inputfile>\n",argv[0]);
        return 1;
    }

    yyin = fopen(argv[1], "r");
    if(!yyin){
        perror("Error opening file");
        return 1;
    }

    yylex();

    printf("%d %d %d %s\n",line_count,word_count,char_count,argv[1]);

    fclose(yyin);
    return 0;
}