NAME : ARNAV MISHRA
ID : 12340330
NAME : AGASTYA NATH
ID : 12340140

This program is a Lex and Yacc-based lexical analyzer and parser that reads a source file (or standard input if no file is given) and identifies tokens such as keywords, identifiers, constants, operators, strings, and comments based on the given language specification and then parses the token stream to check whether the given code is syntactically correct or not.

It uses Flex (lex) for tokenizing and outputs the recognized tokens along with their type and Bison (yacc) for creating the parse tree and hence checking the grammar.

How to Compile and Run:

1. Run the following commands:
   lex ./q.l
   yacc -d ./q.y
   gcc ./lex.yy.c ./y.tab.c
2(a). To run on a file(eg: input.txt):
       ./a.out input.txt
2(b). To run on user input:
      ./a.out   (then type code and press Ctrl+D to end input. Note: after typing code pressing Ctrl+D 			is necessary for getting the output.)
Note:
1. input.txt file is provided for default use.
2. Ensure that lex and yacc are installed in the computer.
3. Ensure that all files are in same folder.

Token Categories:

- Keywords → void, int, double, bool, string, extends, implements, for, while, ReadInteger, ReadLine,
  class, interface, if, else, return, null, this, break, New, NewArray, Print
- Identifiers → Begin with a letter, followed by letters, digits, or underscores (up to 31 characters)
- Boolean Constants → true, false
- Integer Constants → Decimal (123), Hexadecimal (0x1A)
- Double Constants → Examples: 12.34, 3.14e10, -0.5E-3
- String Literals → Enclosed in quotes "Hello World"
- Operators & Symbols → + - * / % \ < <= > >= = == != && || ! ; , . [ ] ( ) { }
- Comments:
  • Single-line: // comment
  • Multi-line: /* comment */
- Whitespace: Ignored (not printed)

Input Constraints:

- File names should be valid and accessible
- Identifiers must follow naming rules (no starting digit, max length 31)
- Strings cannot span multiple lines (must be enclosed within the same line)
- Comments should follow C/Java-style syntax

Example Run:

Input :

class Test{
  int hello;
  void main(){
    if (checks >= 2 && flag == false){
      hello = 3;
    }
  }
}

Output:

Parsing successful