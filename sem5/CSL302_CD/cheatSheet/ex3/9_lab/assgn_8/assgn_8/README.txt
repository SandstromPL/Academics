Name: Agastya Nath
Roll No.: 12340140
Course: CSL302 – Compiler Design

Lab 8 Assignment:

I. Files included:
    1. symbol.c
    2. symbol.h
    3. analyzer.l
    4. parser.y
    5. sample.txt (for demo)
    6. README.txt (this file; for further instructions and knowledge)

II. Instructions to generate the parser:
    1. Compile ./analyzer.l with lex as follows:
        lex ./analyzer.l
    2. Compile ./parser.y with yacc (with option -d) as follows:
        yacc -d ./parser.y
    3. Compile the resultant ./lex.yy.c and ./y.tab.c with gcc along with ./symbol.c as follows:
        gcc ./lex.yy.c ./y.tab.c ./symbol.c
    4. The resultant executable from gcc (./a.out) is the parser.

III. How to use:
    It can be used either interactively (i.e. without any commandline arguments) or with an argument (as source file name passed as argument).
    
    1. If used interactively, enter ./a.out. After that, Enter source code line-by-line until an error is detected (then it detects it with an error and exits). If you 
    want to manually exit the parser, just press Ctrl-C.
    2. If used with a source file, enter ./a.out file_name.txt (eg. ./a.out ./sample.txt). Then it prints all the lines of information and then
    at the end it tells you whether the code is syntactically correct or not.

IV. Assumptions:
    1. Only int and float are supported.
    2. No function scopes implemented.
    3. TAC generation is printed directly; not stored.
    4. Memory for symbols freed only on scope exit.
    5. Scope management added as well.

V. Example:

Example file: ./sample.txt

int a, b, c;
float d, e, f;
a = b * c - d / f;
k = e or f >= g and h != i and not j;

Enter: ./a.out ./sample.txt

Output: 

Declared a of type int in scope 1
Declared b of type int in scope 1
Declared c of type int in scope 1
Declared d of type float in scope 1
Declared e of type float in scope 1
Declared f of type float in scope 1
1: t1 = d / f
2: t2 = c - t1
3: t3 = b * t2
4: a = t3
5: t4 = !j
6: t5 = i && t4
7: if h != t5 goto 10
8: t6 = 0
9: goto 11
10: t6 = 1
11: t7 = g && t6
12: if f >= t7 goto 15
13: t8 = 0
14: goto 16
15: t8 = 1
16: t9 = e || t8
17: k = t9
The above program is syntactically correct


