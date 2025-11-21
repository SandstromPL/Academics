/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_Y_TAB_H_INCLUDED
# define YY_YY_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    INT = 258,                     /* INT  */
    DOUBLE = 259,                  /* DOUBLE  */
    BOOL = 260,                    /* BOOL  */
    STRING = 261,                  /* STRING  */
    VOID = 262,                    /* VOID  */
    IDENTIFIER = 263,              /* IDENTIFIER  */
    HEXA_CONST = 264,              /* HEXA_CONST  */
    INT_CONST = 265,               /* INT_CONST  */
    DOUBLE_CONST = 266,            /* DOUBLE_CONST  */
    STR_CONST = 267,               /* STR_CONST  */
    TRUE_CONST = 268,              /* TRUE_CONST  */
    FALSE_CONST = 269,             /* FALSE_CONST  */
    CLASS = 270,                   /* CLASS  */
    IF = 271,                      /* IF  */
    ELSE = 272,                    /* ELSE  */
    WHILE = 273,                   /* WHILE  */
    FOR = 274,                     /* FOR  */
    DO = 275,                      /* DO  */
    BREAK = 276,                   /* BREAK  */
    RETURN = 277,                  /* RETURN  */
    NEWARRAY = 278,                /* NEWARRAY  */
    NEW = 279,                     /* NEW  */
    MAIN = 280,                    /* MAIN  */
    ASSIGN = 281,                  /* ASSIGN  */
    EQ = 282,                      /* EQ  */
    NEQ = 283,                     /* NEQ  */
    LT = 284,                      /* LT  */
    LE = 285,                      /* LE  */
    GT = 286,                      /* GT  */
    GE = 287,                      /* GE  */
    AND = 288,                     /* AND  */
    OR = 289,                      /* OR  */
    NOT = 290,                     /* NOT  */
    PLUS = 291,                    /* PLUS  */
    MINUS = 292,                   /* MINUS  */
    MUL = 293,                     /* MUL  */
    DIV = 294,                     /* DIV  */
    MOD = 295,                     /* MOD  */
    L_RND_BRC = 296,               /* L_RND_BRC  */
    R_RND_BRC = 297,               /* R_RND_BRC  */
    L_CURL_BRC = 298,              /* L_CURL_BRC  */
    R_CURL_BRC = 299,              /* R_CURL_BRC  */
    L_SQR_BRC = 300,               /* L_SQR_BRC  */
    R_SQR_BRC = 301,               /* R_SQR_BRC  */
    SEMICOLON = 302,               /* SEMICOLON  */
    COMMA = 303,                   /* COMMA  */
    DOT = 304,                     /* DOT  */
    LOWER_THAN_ELSE = 305,         /* LOWER_THAN_ELSE  */
    UMINUS = 306                   /* UMINUS  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif
/* Token kinds.  */
#define YYEMPTY -2
#define YYEOF 0
#define YYerror 256
#define YYUNDEF 257
#define INT 258
#define DOUBLE 259
#define BOOL 260
#define STRING 261
#define VOID 262
#define IDENTIFIER 263
#define HEXA_CONST 264
#define INT_CONST 265
#define DOUBLE_CONST 266
#define STR_CONST 267
#define TRUE_CONST 268
#define FALSE_CONST 269
#define CLASS 270
#define IF 271
#define ELSE 272
#define WHILE 273
#define FOR 274
#define DO 275
#define BREAK 276
#define RETURN 277
#define NEWARRAY 278
#define NEW 279
#define MAIN 280
#define ASSIGN 281
#define EQ 282
#define NEQ 283
#define LT 284
#define LE 285
#define GT 286
#define GE 287
#define AND 288
#define OR 289
#define NOT 290
#define PLUS 291
#define MINUS 292
#define MUL 293
#define DIV 294
#define MOD 295
#define L_RND_BRC 296
#define R_RND_BRC 297
#define L_CURL_BRC 298
#define R_CURL_BRC 299
#define L_SQR_BRC 300
#define R_SQR_BRC 301
#define SEMICOLON 302
#define COMMA 303
#define DOT 304
#define LOWER_THAN_ELSE 305
#define UMINUS 306

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 20 "parser.y"

    char* str;

#line 173 "y.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
