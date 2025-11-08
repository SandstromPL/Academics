
LAB-9: THREE ADDRESS CODE GENERATOR
CSL302: Compiler Design

Name: ASHISH RANJAN
Id: 12340370


FILES INCLUDED:
---------------
1. symbol.h          - Symbol table header file
2. symbol.c          - Symbol table implementation
3. lex.l           - Lex file for lexical analysis
4. parser.y          - Yacc file for parser and TAC generation
5. input.txt          - Sample test cases
6. README.txt        - This file

COMPILATION:
------------
    lex lexer.l
    yacc -d parser.y
    gcc lex.yy.c y.tab.c symbol.c -o final 

RUNNING:
--------
    ./final

With test file:
    ./final < input.txt
