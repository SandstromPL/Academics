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
    IF = 258,                      /* IF  */
    GOTO = 259,                    /* GOTO  */
    IDENTIFIER = 260,              /* IDENTIFIER  */
    TEMP_VAR = 261,                /* TEMP_VAR  */
    CONSTANT = 262,                /* CONSTANT  */
    LABEL = 263,                   /* LABEL  */
    PLUS = 264,                    /* PLUS  */
    MINUS = 265,                   /* MINUS  */
    MULTIPLY = 266,                /* MULTIPLY  */
    DIVIDE = 267,                  /* DIVIDE  */
    LT = 268,                      /* LT  */
    GT = 269,                      /* GT  */
    ASSGN = 270,                   /* ASSGN  */
    NEG = 271,                     /* NEG  */
    EQ = 272,                      /* EQ  */
    NE = 273,                      /* NE  */
    LE = 274,                      /* LE  */
    GE = 275,                      /* GE  */
    LEFT_SQUARE = 276,             /* LEFT_SQUARE  */
    RIGHT_SQUARE = 277,            /* RIGHT_SQUARE  */
    SEMICOLON = 278,               /* SEMICOLON  */
    COLON = 279,                   /* COLON  */
    UMINUS = 280,                  /* UMINUS  */
    NEGATE = 281,                  /* NEGATE  */
    MUL = 282                      /* MUL  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif
/* Token kinds.  */
#define YYEMPTY -2
#define YYEOF 0
#define YYerror 256
#define YYUNDEF 257
#define IF 258
#define GOTO 259
#define IDENTIFIER 260
#define TEMP_VAR 261
#define CONSTANT 262
#define LABEL 263
#define PLUS 264
#define MINUS 265
#define MULTIPLY 266
#define DIVIDE 267
#define LT 268
#define GT 269
#define ASSGN 270
#define NEG 271
#define EQ 272
#define NE 273
#define LE 274
#define GE 275
#define LEFT_SQUARE 276
#define RIGHT_SQUARE 277
#define SEMICOLON 278
#define COLON 279
#define UMINUS 280
#define NEGATE 281
#define MUL 282

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 15 "sol.y"

    char* str;

#line 125 "y.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
