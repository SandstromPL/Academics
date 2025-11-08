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
    ID = 258,                      /* ID  */
    NUM = 259,                     /* NUM  */
    ASSIGN = 260,                  /* ASSIGN  */
    PLUS = 261,                    /* PLUS  */
    MINUS = 262,                   /* MINUS  */
    MULTIPY = 263,                 /* MULTIPY  */
    DIVIDE = 264,                  /* DIVIDE  */
    LBRAC = 265,                   /* LBRAC  */
    RBRAC = 266,                   /* RBRAC  */
    LCURL = 267,                   /* LCURL  */
    RCURL = 268,                   /* RCURL  */
    LT = 269,                      /* LT  */
    GT = 270,                      /* GT  */
    LE = 271,                      /* LE  */
    GE = 272,                      /* GE  */
    NE = 273,                      /* NE  */
    EQ = 274,                      /* EQ  */
    AND = 275,                     /* AND  */
    OR = 276,                      /* OR  */
    NOT = 277,                     /* NOT  */
    TRUE = 278,                    /* TRUE  */
    FALSE = 279,                   /* FALSE  */
    IF = 280,                      /* IF  */
    ELSE = 281,                    /* ELSE  */
    THEN = 282,                    /* THEN  */
    WHILE = 283,                   /* WHILE  */
    INT = 284,                     /* INT  */
    FLOAT = 285,                   /* FLOAT  */
    COMMA = 286,                   /* COMMA  */
    SEMICOLON = 287,               /* SEMICOLON  */
    dangling = 288                 /* dangling  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif
/* Token kinds.  */
#define YYEMPTY -2
#define YYEOF 0
#define YYerror 256
#define YYUNDEF 257
#define ID 258
#define NUM 259
#define ASSIGN 260
#define PLUS 261
#define MINUS 262
#define MULTIPY 263
#define DIVIDE 264
#define LBRAC 265
#define RBRAC 266
#define LCURL 267
#define RCURL 268
#define LT 269
#define GT 270
#define LE 271
#define GE 272
#define NE 273
#define EQ 274
#define AND 275
#define OR 276
#define NOT 277
#define TRUE 278
#define FALSE 279
#define IF 280
#define ELSE 281
#define THEN 282
#define WHILE 283
#define INT 284
#define FLOAT 285
#define COMMA 286
#define SEMICOLON 287
#define dangling 288

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 28 "yacc.y"

    char *str;

    struct{
        char * truelabel;
        char * falselabel;
    }labels;

#line 142 "y.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
