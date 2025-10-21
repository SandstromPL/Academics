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
    TYPE = 258,                    /* TYPE  */
    FOR = 259,                     /* FOR  */
    IF = 260,                      /* IF  */
    ELSE = 261,                    /* ELSE  */
    DO = 262,                      /* DO  */
    WHILE = 263,                   /* WHILE  */
    BOOLEAN = 264,                 /* BOOLEAN  */
    IDENTIFIER = 265,              /* IDENTIFIER  */
    KEYWORD = 266,                 /* KEYWORD  */
    RETURN = 267,                  /* RETURN  */
    BREAK = 268,                   /* BREAK  */
    CLASS = 269,                   /* CLASS  */
    NEW = 270,                     /* NEW  */
    NEW_ARRAY = 271,               /* NEW_ARRAY  */
    DOT = 272,                     /* DOT  */
    COMMA = 273,                   /* COMMA  */
    SINGLE_COMMENT = 274,          /* SINGLE_COMMENT  */
    MULTI_COMMENT = 275,           /* MULTI_COMMENT  */
    STRING = 276,                  /* STRING  */
    INTEGER = 277,                 /* INTEGER  */
    DOUBLE = 278,                  /* DOUBLE  */
    COLON = 279,                   /* COLON  */
    SEMICOLON = 280,               /* SEMICOLON  */
    AND = 281,                     /* AND  */
    OR = 282,                      /* OR  */
    ADD = 283,                     /* ADD  */
    SUBTRACT = 284,                /* SUBTRACT  */
    MULTIPLY = 285,                /* MULTIPLY  */
    DIVIDE = 286,                  /* DIVIDE  */
    REM = 287,                     /* REM  */
    ASSGN = 288,                   /* ASSGN  */
    NEG = 289,                     /* NEG  */
    LT = 290,                      /* LT  */
    GT = 291,                      /* GT  */
    LE = 292,                      /* LE  */
    GE = 293,                      /* GE  */
    EQ = 294,                      /* EQ  */
    NE = 295,                      /* NE  */
    LEFT_BRAC = 296,               /* LEFT_BRAC  */
    RIGHT_BRAC = 297,              /* RIGHT_BRAC  */
    LEFT_PAREN = 298,              /* LEFT_PAREN  */
    RIGHT_PAREN = 299,             /* RIGHT_PAREN  */
    LEFT_SQUARE = 300,             /* LEFT_SQUARE  */
    RIGHT_SQUARE = 301,            /* RIGHT_SQUARE  */
    UMINUS = 302,                  /* UMINUS  */
    NEGATE = 303,                  /* NEGATE  */
    LOWER_THAN_ELSE = 304          /* LOWER_THAN_ELSE  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif
/* Token kinds.  */
#define YYEMPTY -2
#define YYEOF 0
#define YYerror 256
#define YYUNDEF 257
#define TYPE 258
#define FOR 259
#define IF 260
#define ELSE 261
#define DO 262
#define WHILE 263
#define BOOLEAN 264
#define IDENTIFIER 265
#define KEYWORD 266
#define RETURN 267
#define BREAK 268
#define CLASS 269
#define NEW 270
#define NEW_ARRAY 271
#define DOT 272
#define COMMA 273
#define SINGLE_COMMENT 274
#define MULTI_COMMENT 275
#define STRING 276
#define INTEGER 277
#define DOUBLE 278
#define COLON 279
#define SEMICOLON 280
#define AND 281
#define OR 282
#define ADD 283
#define SUBTRACT 284
#define MULTIPLY 285
#define DIVIDE 286
#define REM 287
#define ASSGN 288
#define NEG 289
#define LT 290
#define GT 291
#define LE 292
#define GE 293
#define EQ 294
#define NE 295
#define LEFT_BRAC 296
#define RIGHT_BRAC 297
#define LEFT_PAREN 298
#define RIGHT_PAREN 299
#define LEFT_SQUARE 300
#define RIGHT_SQUARE 301
#define UMINUS 302
#define NEGATE 303
#define LOWER_THAN_ELSE 304

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 31 "q2.y"

    char* str;

#line 169 "y.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
