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
    CLASS = 263,                   /* CLASS  */
    IF = 264,                      /* IF  */
    ELSE = 265,                    /* ELSE  */
    WHILE = 266,                   /* WHILE  */
    FOR = 267,                     /* FOR  */
    DO = 268,                      /* DO  */
    BREAK = 269,                   /* BREAK  */
    RETURN = 270,                  /* RETURN  */
    NEWARRAY = 271,                /* NEWARRAY  */
    NEW = 272,                     /* NEW  */
    MAIN = 273,                    /* MAIN  */
    ASSIGN = 274,                  /* ASSIGN  */
    EQ = 275,                      /* EQ  */
    NEQ = 276,                     /* NEQ  */
    LT = 277,                      /* LT  */
    LE = 278,                      /* LE  */
    GT = 279,                      /* GT  */
    GE = 280,                      /* GE  */
    AND = 281,                     /* AND  */
    OR = 282,                      /* OR  */
    NOT = 283,                     /* NOT  */
    PLUS = 284,                    /* PLUS  */
    MINUS = 285,                   /* MINUS  */
    MUL = 286,                     /* MUL  */
    DIV = 287,                     /* DIV  */
    MOD = 288,                     /* MOD  */
    L_RND_BRC = 289,               /* L_RND_BRC  */
    R_RND_BRC = 290,               /* R_RND_BRC  */
    L_CURL_BRC = 291,              /* L_CURL_BRC  */
    R_CURL_BRC = 292,              /* R_CURL_BRC  */
    L_SQR_BRC = 293,               /* L_SQR_BRC  */
    R_SQR_BRC = 294,               /* R_SQR_BRC  */
    SEMICOLON = 295,               /* SEMICOLON  */
    COMMA = 296,                   /* COMMA  */
    DOT = 297,                     /* DOT  */
    IDENTIFIER = 298,              /* IDENTIFIER  */
    HEXA_CONST = 299,              /* HEXA_CONST  */
    INT_CONST = 300,               /* INT_CONST  */
    DOUBLE_CONST = 301,            /* DOUBLE_CONST  */
    STR_CONST = 302,               /* STR_CONST  */
    TRUE_CONST = 303,              /* TRUE_CONST  */
    FALSE_CONST = 304,             /* FALSE_CONST  */
    UMINUS = 305,                  /* UMINUS  */
    IFX = 306                      /* IFX  */
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
#define CLASS 263
#define IF 264
#define ELSE 265
#define WHILE 266
#define FOR 267
#define DO 268
#define BREAK 269
#define RETURN 270
#define NEWARRAY 271
#define NEW 272
#define MAIN 273
#define ASSIGN 274
#define EQ 275
#define NEQ 276
#define LT 277
#define LE 278
#define GT 279
#define GE 280
#define AND 281
#define OR 282
#define NOT 283
#define PLUS 284
#define MINUS 285
#define MUL 286
#define DIV 287
#define MOD 288
#define L_RND_BRC 289
#define R_RND_BRC 290
#define L_CURL_BRC 291
#define R_CURL_BRC 292
#define L_SQR_BRC 293
#define R_SQR_BRC 294
#define SEMICOLON 295
#define COMMA 296
#define DOT 297
#define IDENTIFIER 298
#define HEXA_CONST 299
#define INT_CONST 300
#define DOUBLE_CONST 301
#define STR_CONST 302
#define TRUE_CONST 303
#define FALSE_CONST 304
#define UMINUS 305
#define IFX 306

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
