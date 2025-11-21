/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison implementation for Yacc-like parsers in C

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

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output, and Bison version.  */
#define YYBISON 30802

/* Bison version string.  */
#define YYBISON_VERSION "3.8.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1




/* First part of user prologue.  */
#line 1 "parser.y"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symbol.h" 

void yyerror(const char *s);
int yylex(void);
extern int yylineno;

// --- HELPER FUNCTIONS ---
int temp_count = 0;
int label_count = 0;
char* new_temp();
char* new_label();
void check_scope(char* id);

#line 89 "y.tab.c"

# ifndef YY_CAST
#  ifdef __cplusplus
#   define YY_CAST(Type, Val) static_cast<Type> (Val)
#   define YY_REINTERPRET_CAST(Type, Val) reinterpret_cast<Type> (Val)
#  else
#   define YY_CAST(Type, Val) ((Type) (Val))
#   define YY_REINTERPRET_CAST(Type, Val) ((Type) (Val))
#  endif
# endif
# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

/* Use api.header.include to #include this header
   instead of duplicating it here.  */
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

#line 248 "y.tab.c"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
/* Symbol kind.  */
enum yysymbol_kind_t
{
  YYSYMBOL_YYEMPTY = -2,
  YYSYMBOL_YYEOF = 0,                      /* "end of file"  */
  YYSYMBOL_YYerror = 1,                    /* error  */
  YYSYMBOL_YYUNDEF = 2,                    /* "invalid token"  */
  YYSYMBOL_INT = 3,                        /* INT  */
  YYSYMBOL_DOUBLE = 4,                     /* DOUBLE  */
  YYSYMBOL_BOOL = 5,                       /* BOOL  */
  YYSYMBOL_STRING = 6,                     /* STRING  */
  YYSYMBOL_VOID = 7,                       /* VOID  */
  YYSYMBOL_IDENTIFIER = 8,                 /* IDENTIFIER  */
  YYSYMBOL_HEXA_CONST = 9,                 /* HEXA_CONST  */
  YYSYMBOL_INT_CONST = 10,                 /* INT_CONST  */
  YYSYMBOL_DOUBLE_CONST = 11,              /* DOUBLE_CONST  */
  YYSYMBOL_STR_CONST = 12,                 /* STR_CONST  */
  YYSYMBOL_TRUE_CONST = 13,                /* TRUE_CONST  */
  YYSYMBOL_FALSE_CONST = 14,               /* FALSE_CONST  */
  YYSYMBOL_CLASS = 15,                     /* CLASS  */
  YYSYMBOL_IF = 16,                        /* IF  */
  YYSYMBOL_ELSE = 17,                      /* ELSE  */
  YYSYMBOL_WHILE = 18,                     /* WHILE  */
  YYSYMBOL_FOR = 19,                       /* FOR  */
  YYSYMBOL_DO = 20,                        /* DO  */
  YYSYMBOL_BREAK = 21,                     /* BREAK  */
  YYSYMBOL_RETURN = 22,                    /* RETURN  */
  YYSYMBOL_NEWARRAY = 23,                  /* NEWARRAY  */
  YYSYMBOL_NEW = 24,                       /* NEW  */
  YYSYMBOL_MAIN = 25,                      /* MAIN  */
  YYSYMBOL_ASSIGN = 26,                    /* ASSIGN  */
  YYSYMBOL_EQ = 27,                        /* EQ  */
  YYSYMBOL_NEQ = 28,                       /* NEQ  */
  YYSYMBOL_LT = 29,                        /* LT  */
  YYSYMBOL_LE = 30,                        /* LE  */
  YYSYMBOL_GT = 31,                        /* GT  */
  YYSYMBOL_GE = 32,                        /* GE  */
  YYSYMBOL_AND = 33,                       /* AND  */
  YYSYMBOL_OR = 34,                        /* OR  */
  YYSYMBOL_NOT = 35,                       /* NOT  */
  YYSYMBOL_PLUS = 36,                      /* PLUS  */
  YYSYMBOL_MINUS = 37,                     /* MINUS  */
  YYSYMBOL_MUL = 38,                       /* MUL  */
  YYSYMBOL_DIV = 39,                       /* DIV  */
  YYSYMBOL_MOD = 40,                       /* MOD  */
  YYSYMBOL_L_RND_BRC = 41,                 /* L_RND_BRC  */
  YYSYMBOL_R_RND_BRC = 42,                 /* R_RND_BRC  */
  YYSYMBOL_L_CURL_BRC = 43,                /* L_CURL_BRC  */
  YYSYMBOL_R_CURL_BRC = 44,                /* R_CURL_BRC  */
  YYSYMBOL_L_SQR_BRC = 45,                 /* L_SQR_BRC  */
  YYSYMBOL_R_SQR_BRC = 46,                 /* R_SQR_BRC  */
  YYSYMBOL_SEMICOLON = 47,                 /* SEMICOLON  */
  YYSYMBOL_COMMA = 48,                     /* COMMA  */
  YYSYMBOL_DOT = 49,                       /* DOT  */
  YYSYMBOL_LOWER_THAN_ELSE = 50,           /* LOWER_THAN_ELSE  */
  YYSYMBOL_UMINUS = 51,                    /* UMINUS  */
  YYSYMBOL_YYACCEPT = 52,                  /* $accept  */
  YYSYMBOL_M = 53,                         /* M  */
  YYSYMBOL_Program = 54,                   /* Program  */
  YYSYMBOL_DeclList = 55,                  /* DeclList  */
  YYSYMBOL_Decl = 56,                      /* Decl  */
  YYSYMBOL_VarDecl = 57,                   /* VarDecl  */
  YYSYMBOL_FuncDecl = 58,                  /* FuncDecl  */
  YYSYMBOL_ClassDecl = 59,                 /* ClassDecl  */
  YYSYMBOL_Fields = 60,                    /* Fields  */
  YYSYMBOL_Field = 61,                     /* Field  */
  YYSYMBOL_MainFunc = 62,                  /* MainFunc  */
  YYSYMBOL_FormalsParam = 63,              /* FormalsParam  */
  YYSYMBOL_FormalsList = 64,               /* FormalsList  */
  YYSYMBOL_StmtBlock = 65,                 /* StmtBlock  */
  YYSYMBOL_BlockContent = 66,              /* BlockContent  */
  YYSYMBOL_BlockItem = 67,                 /* BlockItem  */
  YYSYMBOL_Stmt = 68,                      /* Stmt  */
  YYSYMBOL_IfHead = 69,                    /* IfHead  */
  YYSYMBOL_IfStmt = 70,                    /* IfStmt  */
  YYSYMBOL_71_1 = 71,                      /* $@1  */
  YYSYMBOL_WhileStmt = 72,                 /* WhileStmt  */
  YYSYMBOL_73_2 = 73,                      /* @2  */
  YYSYMBOL_DoWhileStmt = 74,               /* DoWhileStmt  */
  YYSYMBOL_ForStmt = 75,                   /* ForStmt  */
  YYSYMBOL_76_3 = 76,                      /* @3  */
  YYSYMBOL_ExprFor = 77,                   /* ExprFor  */
  YYSYMBOL_BreakStmt = 78,                 /* BreakStmt  */
  YYSYMBOL_ReturnStmt = 79,                /* ReturnStmt  */
  YYSYMBOL_ExprOpt = 80,                   /* ExprOpt  */
  YYSYMBOL_Type = 81,                      /* Type  */
  YYSYMBOL_Expr = 82,                      /* Expr  */
  YYSYMBOL_LValue = 83,                    /* LValue  */
  YYSYMBOL_Call = 84,                      /* Call  */
  YYSYMBOL_Actuals = 85,                   /* Actuals  */
  YYSYMBOL_ActualList = 86,                /* ActualList  */
  YYSYMBOL_Constant = 87                   /* Constant  */
};
typedef enum yysymbol_kind_t yysymbol_kind_t;




#ifdef short
# undef short
#endif

/* On compilers that do not define __PTRDIFF_MAX__ etc., make sure
   <limits.h> and (if available) <stdint.h> are included
   so that the code can choose integer types of a good width.  */

#ifndef __PTRDIFF_MAX__
# include <limits.h> /* INFRINGES ON USER NAME SPACE */
# if defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stdint.h> /* INFRINGES ON USER NAME SPACE */
#  define YY_STDINT_H
# endif
#endif

/* Narrow types that promote to a signed type and that can represent a
   signed or unsigned integer of at least N bits.  In tables they can
   save space and decrease cache pressure.  Promoting to a signed type
   helps avoid bugs in integer arithmetic.  */

#ifdef __INT_LEAST8_MAX__
typedef __INT_LEAST8_TYPE__ yytype_int8;
#elif defined YY_STDINT_H
typedef int_least8_t yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef __INT_LEAST16_MAX__
typedef __INT_LEAST16_TYPE__ yytype_int16;
#elif defined YY_STDINT_H
typedef int_least16_t yytype_int16;
#else
typedef short yytype_int16;
#endif

/* Work around bug in HP-UX 11.23, which defines these macros
   incorrectly for preprocessor constants.  This workaround can likely
   be removed in 2023, as HPE has promised support for HP-UX 11.23
   (aka HP-UX 11i v2) only through the end of 2022; see Table 2 of
   <https://h20195.www2.hpe.com/V2/getpdf.aspx/4AA4-7673ENW.pdf>.  */
#ifdef __hpux
# undef UINT_LEAST8_MAX
# undef UINT_LEAST16_MAX
# define UINT_LEAST8_MAX 255
# define UINT_LEAST16_MAX 65535
#endif

#if defined __UINT_LEAST8_MAX__ && __UINT_LEAST8_MAX__ <= __INT_MAX__
typedef __UINT_LEAST8_TYPE__ yytype_uint8;
#elif (!defined __UINT_LEAST8_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST8_MAX <= INT_MAX)
typedef uint_least8_t yytype_uint8;
#elif !defined __UINT_LEAST8_MAX__ && UCHAR_MAX <= INT_MAX
typedef unsigned char yytype_uint8;
#else
typedef short yytype_uint8;
#endif

#if defined __UINT_LEAST16_MAX__ && __UINT_LEAST16_MAX__ <= __INT_MAX__
typedef __UINT_LEAST16_TYPE__ yytype_uint16;
#elif (!defined __UINT_LEAST16_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST16_MAX <= INT_MAX)
typedef uint_least16_t yytype_uint16;
#elif !defined __UINT_LEAST16_MAX__ && USHRT_MAX <= INT_MAX
typedef unsigned short yytype_uint16;
#else
typedef int yytype_uint16;
#endif

#ifndef YYPTRDIFF_T
# if defined __PTRDIFF_TYPE__ && defined __PTRDIFF_MAX__
#  define YYPTRDIFF_T __PTRDIFF_TYPE__
#  define YYPTRDIFF_MAXIMUM __PTRDIFF_MAX__
# elif defined PTRDIFF_MAX
#  ifndef ptrdiff_t
#   include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  endif
#  define YYPTRDIFF_T ptrdiff_t
#  define YYPTRDIFF_MAXIMUM PTRDIFF_MAX
# else
#  define YYPTRDIFF_T long
#  define YYPTRDIFF_MAXIMUM LONG_MAX
# endif
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM                                  \
  YY_CAST (YYPTRDIFF_T,                                 \
           (YYPTRDIFF_MAXIMUM < YY_CAST (YYSIZE_T, -1)  \
            ? YYPTRDIFF_MAXIMUM                         \
            : YY_CAST (YYSIZE_T, -1)))

#define YYSIZEOF(X) YY_CAST (YYPTRDIFF_T, sizeof (X))


/* Stored state numbers (used for stacks). */
typedef yytype_uint8 yy_state_t;

/* State numbers in computations.  */
typedef int yy_state_fast_t;

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif


#ifndef YY_ATTRIBUTE_PURE
# if defined __GNUC__ && 2 < __GNUC__ + (96 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_PURE __attribute__ ((__pure__))
# else
#  define YY_ATTRIBUTE_PURE
# endif
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# if defined __GNUC__ && 2 < __GNUC__ + (7 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_UNUSED __attribute__ ((__unused__))
# else
#  define YY_ATTRIBUTE_UNUSED
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YY_USE(E) ((void) (E))
#else
# define YY_USE(E) /* empty */
#endif

/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
#if defined __GNUC__ && ! defined __ICC && 406 <= __GNUC__ * 100 + __GNUC_MINOR__
# if __GNUC__ * 100 + __GNUC_MINOR__ < 407
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")
# else
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")              \
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# endif
# define YY_IGNORE_MAYBE_UNINITIALIZED_END      \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif

#if defined __cplusplus && defined __GNUC__ && ! defined __ICC && 6 <= __GNUC__
# define YY_IGNORE_USELESS_CAST_BEGIN                          \
    _Pragma ("GCC diagnostic push")                            \
    _Pragma ("GCC diagnostic ignored \"-Wuseless-cast\"")
# define YY_IGNORE_USELESS_CAST_END            \
    _Pragma ("GCC diagnostic pop")
#endif
#ifndef YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_END
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if !defined yyoverflow

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* !defined yyoverflow */

#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yy_state_t yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (YYSIZEOF (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (YYSIZEOF (yy_state_t) + YYSIZEOF (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYPTRDIFF_T yynewbytes;                                         \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * YYSIZEOF (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / YYSIZEOF (*yyptr);                        \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, YY_CAST (YYSIZE_T, (Count)) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYPTRDIFF_T yyi;                      \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  3
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   423

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  52
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  36
/* YYNRULES -- Number of rules.  */
#define YYNRULES  93
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  181

/* YYMAXUTOK -- Last valid token kind.  */
#define YYMAXUTOK   306


/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                \
  (0 <= (YYX) && (YYX) <= YYMAXUTOK                     \
   ? YY_CAST (yysymbol_kind_t, yytranslate[YYX])        \
   : YYSYMBOL_YYUNDEF)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_int8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51
};

#if YYDEBUG
/* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_int16 yyrline[] =
{
       0,    56,    56,    63,    66,    68,    72,    73,    74,    78,
      81,    85,    89,    95,    99,   102,   104,   108,   109,   113,
     116,   118,   122,   123,   127,   130,   132,   136,   137,   141,
     142,   143,   144,   145,   146,   147,   148,   149,   154,   160,
     163,   163,   174,   174,   185,   191,   191,   212,   213,   217,
     221,   227,   228,   232,   232,   232,   232,   232,   237,   241,
     245,   249,   250,   251,   252,   253,   254,   255,   259,   260,
     261,   262,   263,   264,   265,   266,   270,   271,   272,   279,
     280,   284,   291,   295,   300,   302,   306,   307,   311,   311,
     311,   311,   311,   311
};
#endif

/** Accessing symbol of state STATE.  */
#define YY_ACCESSING_SYMBOL(State) YY_CAST (yysymbol_kind_t, yystos[State])

#if YYDEBUG || 0
/* The user-facing name of the symbol whose (internal) number is
   YYSYMBOL.  No bounds checking.  */
static const char *yysymbol_name (yysymbol_kind_t yysymbol) YY_ATTRIBUTE_UNUSED;

/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "\"end of file\"", "error", "\"invalid token\"", "INT", "DOUBLE",
  "BOOL", "STRING", "VOID", "IDENTIFIER", "HEXA_CONST", "INT_CONST",
  "DOUBLE_CONST", "STR_CONST", "TRUE_CONST", "FALSE_CONST", "CLASS", "IF",
  "ELSE", "WHILE", "FOR", "DO", "BREAK", "RETURN", "NEWARRAY", "NEW",
  "MAIN", "ASSIGN", "EQ", "NEQ", "LT", "LE", "GT", "GE", "AND", "OR",
  "NOT", "PLUS", "MINUS", "MUL", "DIV", "MOD", "L_RND_BRC", "R_RND_BRC",
  "L_CURL_BRC", "R_CURL_BRC", "L_SQR_BRC", "R_SQR_BRC", "SEMICOLON",
  "COMMA", "DOT", "LOWER_THAN_ELSE", "UMINUS", "$accept", "M", "Program",
  "DeclList", "Decl", "VarDecl", "FuncDecl", "ClassDecl", "Fields",
  "Field", "MainFunc", "FormalsParam", "FormalsList", "StmtBlock",
  "BlockContent", "BlockItem", "Stmt", "IfHead", "IfStmt", "$@1",
  "WhileStmt", "@2", "DoWhileStmt", "ForStmt", "@3", "ExprFor",
  "BreakStmt", "ReturnStmt", "ExprOpt", "Type", "Expr", "LValue", "Call",
  "Actuals", "ActualList", "Constant", YY_NULLPTR
};

static const char *
yysymbol_name (yysymbol_kind_t yysymbol)
{
  return yytname[yysymbol];
}
#endif

#define YYPACT_NINF (-144)

#define yypact_value_is_default(Yyn) \
  ((Yyn) == YYPACT_NINF)

#define YYTABLE_NINF (-1)

#define yytable_value_is_error(Yyn) \
  ((Yyn) == YYTABLE_NINF)

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
static const yytype_int16 yypact[] =
{
    -144,    28,   171,  -144,  -144,  -144,  -144,  -144,    12,    75,
      50,  -144,  -144,  -144,  -144,  -144,    51,    19,   -11,    21,
      22,   -16,    24,    23,  -144,    57,  -144,   102,  -144,    43,
      82,    44,    11,  -144,    52,    47,    89,  -144,  -144,    59,
     102,  -144,  -144,  -144,  -144,    43,   102,  -144,   108,    55,
      61,  -144,   117,    15,  -144,  -144,  -144,  -144,  -144,  -144,
      90,    92,    93,  -144,    88,    -2,    97,    -2,    -2,    -2,
    -144,  -144,  -144,  -144,  -144,  -144,   148,  -144,  -144,  -144,
    -144,  -144,  -144,   129,    42,   121,  -144,  -144,  -144,   106,
    -144,    -2,    -2,  -144,    -2,   148,  -144,   107,   116,   284,
     146,   -15,   -15,   169,   154,   118,    -2,    -2,    -2,    -2,
      -2,    -2,    -2,    -2,    -2,    -2,    -2,    -2,    -2,    -2,
    -144,   165,    -2,  -144,   284,   138,   133,   192,    -2,   135,
     284,   166,  -144,   145,  -144,  -144,   330,   330,   374,   374,
     374,   374,   353,   307,   101,   101,   -15,   -15,   -15,   215,
     147,   284,  -144,    -2,  -144,   238,  -144,   149,  -144,   148,
    -144,    -2,   284,  -144,    -2,    -2,  -144,   150,   148,   157,
     261,  -144,  -144,  -144,   163,    -2,  -144,   151,  -144,   148,
    -144
};

/* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE does not specify something else to do.  Zero
   means the default is an error.  */
static const yytype_int8 yydefact[] =
{
       4,     0,     0,     1,    53,    54,    55,    56,    57,     0,
       0,     5,     6,     7,     8,     3,     0,     0,     0,     0,
       0,     0,     0,     0,    12,     0,    15,    20,     9,     0,
       0,     0,     0,    57,     0,    21,     0,    25,    19,     0,
       0,    14,    17,    18,    16,     0,     0,    22,     0,     0,
       0,    13,     0,    79,    90,    88,    91,    89,    92,    93,
       0,     0,     0,     2,     0,    51,     0,     0,     0,     0,
      24,    37,    27,    36,    26,    28,     0,    30,    31,    32,
      33,    34,    35,     0,     0,    75,    76,    77,    11,     0,
      23,    84,     0,     2,    47,     0,    49,    79,     0,    52,
       0,    72,    73,     0,    39,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
      29,     0,     0,    10,    86,     0,    85,     0,     0,     0,
      48,     0,    50,     0,    74,    40,    61,    62,    63,    64,
      65,    66,    60,    59,    67,    68,    69,    70,    71,     0,
      80,    58,    82,     0,    38,     0,     2,     0,    78,     0,
      81,    84,    87,    42,    47,     0,    41,     0,     0,     0,
       0,    83,    43,     2,     0,    47,    44,     0,    45,     0,
      46
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -144,   -88,  -144,  -144,  -144,    -8,   162,  -144,  -144,  -144,
    -144,  -144,  -144,    32,  -144,  -144,   -75,  -144,  -144,  -144,
    -144,  -144,  -144,  -144,  -144,  -143,  -144,  -144,  -144,    96,
     -65,  -144,  -144,    54,  -144,  -144
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_uint8 yydefgoto[] =
{
       0,    95,     1,     2,    11,    12,    13,    14,    32,    44,
      15,    34,    35,    73,    48,    74,    75,    76,    77,   159,
      78,   168,    79,    80,   179,   129,    81,    82,    98,    16,
      84,    85,    86,   125,   126,    87
};

/* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule whose
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int16 yytable[] =
{
      99,   104,   101,   102,   103,   128,    97,    54,    55,    56,
      57,    58,    59,    23,     4,     5,     6,     7,    33,     9,
     131,   169,    66,    18,    42,    27,   124,   127,     3,   130,
     119,    28,   177,    67,   121,    68,    24,    17,    19,    69,
      72,   136,   137,   138,   139,   140,   141,   142,   143,   144,
     145,   146,   147,   148,   149,    41,    91,   151,    20,    21,
      22,    38,    25,   155,    30,    26,    29,    31,   164,   106,
     107,   108,   109,   110,   111,   112,   113,    51,   114,   115,
     116,   117,   118,    18,   166,   175,    37,   119,   162,   120,
      39,   121,    40,   172,    45,    46,   124,    47,    19,   130,
     170,    49,    88,    89,   180,     4,     5,     6,     7,    33,
     130,     4,     5,     6,     7,    33,    53,    54,    55,    56,
      57,    58,    59,    36,    60,    90,    61,    62,    63,    64,
      65,    92,    66,    93,    94,    96,    50,   105,   100,   116,
     117,   118,    52,    67,    83,    68,   119,   122,    91,    69,
     121,    37,    70,   123,   133,    71,    97,    54,    55,    56,
      57,    58,    59,   132,    60,    28,    61,    62,    63,    64,
      65,   135,    66,   150,     4,     5,     6,     7,     8,     9,
     152,   153,   156,    67,   157,    68,    10,   158,   161,    69,
     165,    37,   171,   178,    43,    71,   106,   107,   108,   109,
     110,   111,   112,   113,   173,   114,   115,   116,   117,   118,
     176,   134,     0,     0,   119,   167,     0,     0,   121,   106,
     107,   108,   109,   110,   111,   112,   113,     0,   114,   115,
     116,   117,   118,     0,   154,     0,     0,   119,     0,     0,
       0,   121,   106,   107,   108,   109,   110,   111,   112,   113,
       0,   114,   115,   116,   117,   118,     0,     0,     0,     0,
     119,   160,     0,     0,   121,   106,   107,   108,   109,   110,
     111,   112,   113,     0,   114,   115,   116,   117,   118,     0,
     163,     0,     0,   119,     0,     0,     0,   121,   106,   107,
     108,   109,   110,   111,   112,   113,     0,   114,   115,   116,
     117,   118,     0,   174,     0,     0,   119,     0,     0,     0,
     121,   106,   107,   108,   109,   110,   111,   112,   113,     0,
     114,   115,   116,   117,   118,     0,     0,     0,     0,   119,
       0,     0,     0,   121,   106,   107,   108,   109,   110,   111,
     112,     0,     0,   114,   115,   116,   117,   118,     0,     0,
       0,     0,   119,     0,     0,     0,   121,    -1,    -1,   108,
     109,   110,   111,     0,     0,     0,   114,   115,   116,   117,
     118,     0,     0,     0,     0,   119,     0,     0,     0,   121,
     106,   107,   108,   109,   110,   111,     0,     0,     0,   114,
     115,   116,   117,   118,     0,     0,     0,     0,   119,     0,
       0,     0,   121,    -1,    -1,    -1,    -1,     0,     0,     0,
     114,   115,   116,   117,   118,     0,     0,     0,     0,   119,
       0,     0,     0,   121
};

static const yytype_int16 yycheck[] =
{
      65,    76,    67,    68,    69,    93,     8,     9,    10,    11,
      12,    13,    14,    24,     3,     4,     5,     6,     7,     8,
      95,   164,    24,     8,    32,    41,    91,    92,     0,    94,
      45,    47,   175,    35,    49,    37,    47,    25,    23,    41,
      48,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,    44,    41,   122,     8,     8,
      41,    29,    41,   128,    41,    43,    42,    10,   156,    27,
      28,    29,    30,    31,    32,    33,    34,    45,    36,    37,
      38,    39,    40,     8,   159,   173,    43,    45,   153,    47,
       8,    49,    48,   168,    42,    48,   161,     8,    23,   164,
     165,    42,    47,    42,   179,     3,     4,     5,     6,     7,
     175,     3,     4,     5,     6,     7,     8,     9,    10,    11,
      12,    13,    14,    27,    16,     8,    18,    19,    20,    21,
      22,    41,    24,    41,    41,    47,    40,     8,    41,    38,
      39,    40,    46,    35,    48,    37,    45,    26,    41,    41,
      49,    43,    44,    47,     8,    47,     8,     9,    10,    11,
      12,    13,    14,    47,    16,    47,    18,    19,    20,    21,
      22,    17,    24,     8,     3,     4,     5,     6,     7,     8,
      42,    48,    47,    35,    18,    37,    15,    42,    41,    41,
      41,    43,    42,    42,    32,    47,    27,    28,    29,    30,
      31,    32,    33,    34,    47,    36,    37,    38,    39,    40,
      47,    42,    -1,    -1,    45,   161,    -1,    -1,    49,    27,
      28,    29,    30,    31,    32,    33,    34,    -1,    36,    37,
      38,    39,    40,    -1,    42,    -1,    -1,    45,    -1,    -1,
      -1,    49,    27,    28,    29,    30,    31,    32,    33,    34,
      -1,    36,    37,    38,    39,    40,    -1,    -1,    -1,    -1,
      45,    46,    -1,    -1,    49,    27,    28,    29,    30,    31,
      32,    33,    34,    -1,    36,    37,    38,    39,    40,    -1,
      42,    -1,    -1,    45,    -1,    -1,    -1,    49,    27,    28,
      29,    30,    31,    32,    33,    34,    -1,    36,    37,    38,
      39,    40,    -1,    42,    -1,    -1,    45,    -1,    -1,    -1,
      49,    27,    28,    29,    30,    31,    32,    33,    34,    -1,
      36,    37,    38,    39,    40,    -1,    -1,    -1,    -1,    45,
      -1,    -1,    -1,    49,    27,    28,    29,    30,    31,    32,
      33,    -1,    -1,    36,    37,    38,    39,    40,    -1,    -1,
      -1,    -1,    45,    -1,    -1,    -1,    49,    27,    28,    29,
      30,    31,    32,    -1,    -1,    -1,    36,    37,    38,    39,
      40,    -1,    -1,    -1,    -1,    45,    -1,    -1,    -1,    49,
      27,    28,    29,    30,    31,    32,    -1,    -1,    -1,    36,
      37,    38,    39,    40,    -1,    -1,    -1,    -1,    45,    -1,
      -1,    -1,    49,    29,    30,    31,    32,    -1,    -1,    -1,
      36,    37,    38,    39,    40,    -1,    -1,    -1,    -1,    45,
      -1,    -1,    -1,    49
};

/* YYSTOS[STATE-NUM] -- The symbol kind of the accessing symbol of
   state STATE-NUM.  */
static const yytype_int8 yystos[] =
{
       0,    54,    55,     0,     3,     4,     5,     6,     7,     8,
      15,    56,    57,    58,    59,    62,    81,    25,     8,    23,
       8,     8,    41,    24,    47,    41,    43,    41,    47,    42,
      41,    10,    60,     7,    63,    64,    81,    43,    65,     8,
      48,    44,    57,    58,    61,    42,    48,     8,    66,    42,
      81,    65,    81,     8,     9,    10,    11,    12,    13,    14,
      16,    18,    19,    20,    21,    22,    24,    35,    37,    41,
      44,    47,    57,    65,    67,    68,    69,    70,    72,    74,
      75,    78,    79,    81,    82,    83,    84,    87,    47,    42,
       8,    41,    41,    41,    41,    53,    47,     8,    80,    82,
      41,    82,    82,    82,    68,     8,    27,    28,    29,    30,
      31,    32,    33,    34,    36,    37,    38,    39,    40,    45,
      47,    49,    26,    47,    82,    85,    86,    82,    53,    77,
      82,    68,    47,     8,    42,    17,    82,    82,    82,    82,
      82,    82,    82,    82,    82,    82,    82,    82,    82,    82,
       8,    82,    42,    48,    42,    82,    47,    18,    42,    71,
      46,    41,    82,    42,    53,    41,    68,    85,    73,    77,
      82,    42,    68,    47,    42,    53,    47,    77,    42,    76,
      68
};

/* YYR1[RULE-NUM] -- Symbol kind of the left-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr1[] =
{
       0,    52,    53,    54,    55,    55,    56,    56,    56,    57,
      57,    57,    57,    58,    59,    60,    60,    61,    61,    62,
      63,    63,    64,    64,    65,    66,    66,    67,    67,    68,
      68,    68,    68,    68,    68,    68,    68,    68,    69,    70,
      71,    70,    73,    72,    74,    76,    75,    77,    77,    78,
      79,    80,    80,    81,    81,    81,    81,    81,    82,    82,
      82,    82,    82,    82,    82,    82,    82,    82,    82,    82,
      82,    82,    82,    82,    82,    82,    82,    82,    82,    83,
      83,    83,    84,    84,    85,    85,    86,    86,    87,    87,
      87,    87,    87,    87
};

/* YYR2[RULE-NUM] -- Number of symbols on the right-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr2[] =
{
       0,     2,     0,     2,     0,     2,     1,     1,     1,     3,
       8,     7,     3,     6,     5,     0,     2,     1,     1,     5,
       0,     1,     2,     4,     3,     0,     2,     1,     1,     2,
       1,     1,     1,     1,     1,     1,     1,     1,     4,     2,
       0,     5,     0,     7,     8,     0,    12,     0,     1,     2,
       3,     0,     1,     1,     1,     1,     1,     1,     3,     3,
       3,     3,     3,     3,     3,     3,     3,     3,     3,     3,
       3,     3,     2,     2,     3,     1,     1,     1,     4,     1,
       3,     4,     4,     6,     0,     1,     1,     3,     1,     1,
       1,     1,     1,     1
};


enum { YYENOMEM = -2 };

#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYNOMEM         goto yyexhaustedlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Backward compatibility with an undocumented macro.
   Use YYerror or YYUNDEF. */
#define YYERRCODE YYUNDEF


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)




# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Kind, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo,
                       yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  FILE *yyoutput = yyo;
  YY_USE (yyoutput);
  if (!yyvaluep)
    return;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo,
                 yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyo, "%s %s (",
             yykind < YYNTOKENS ? "token" : "nterm", yysymbol_name (yykind));

  yy_symbol_value_print (yyo, yykind, yyvaluep);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yy_state_t *yybottom, yy_state_t *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yy_state_t *yyssp, YYSTYPE *yyvsp,
                 int yyrule)
{
  int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %d):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       YY_ACCESSING_SYMBOL (+yyssp[yyi + 1 - yynrhs]),
                       &yyvsp[(yyi + 1) - (yynrhs)]);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args) ((void) 0)
# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif






/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg,
            yysymbol_kind_t yykind, YYSTYPE *yyvaluep)
{
  YY_USE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yykind, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/* Lookahead token kind.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;




/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    yy_state_fast_t yystate = 0;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus = 0;

    /* Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* Their size.  */
    YYPTRDIFF_T yystacksize = YYINITDEPTH;

    /* The state stack: array, bottom, top.  */
    yy_state_t yyssa[YYINITDEPTH];
    yy_state_t *yyss = yyssa;
    yy_state_t *yyssp = yyss;

    /* The semantic value stack: array, bottom, top.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs = yyvsa;
    YYSTYPE *yyvsp = yyvs;

  int yyn;
  /* The return value of yyparse.  */
  int yyresult;
  /* Lookahead symbol kind.  */
  yysymbol_kind_t yytoken = YYSYMBOL_YYEMPTY;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yychar = YYEMPTY; /* Cause a token to be read.  */

  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yysetstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  YY_IGNORE_USELESS_CAST_BEGIN
  *yyssp = YY_CAST (yy_state_t, yystate);
  YY_IGNORE_USELESS_CAST_END
  YY_STACK_PRINT (yyss, yyssp);

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    YYNOMEM;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYPTRDIFF_T yysize = yyssp - yyss + 1;

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        yy_state_t *yyss1 = yyss;
        YYSTYPE *yyvs1 = yyvs;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * YYSIZEOF (*yyssp),
                    &yyvs1, yysize * YYSIZEOF (*yyvsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        YYNOMEM;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yy_state_t *yyss1 = yyss;
        union yyalloc *yyptr =
          YY_CAST (union yyalloc *,
                   YYSTACK_ALLOC (YY_CAST (YYSIZE_T, YYSTACK_BYTES (yystacksize))));
        if (! yyptr)
          YYNOMEM;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YY_IGNORE_USELESS_CAST_BEGIN
      YYDPRINTF ((stderr, "Stack size increased to %ld\n",
                  YY_CAST (long, yystacksize)));
      YY_IGNORE_USELESS_CAST_END

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */


  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either empty, or end-of-input, or a valid lookahead.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token\n"));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = YYEOF;
      yytoken = YYSYMBOL_YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else if (yychar == YYerror)
    {
      /* The scanner already issued an error message, process directly
         to error recovery.  But do not keep the error token as
         lookahead, it is too special and may lead us to an endless
         loop in error recovery. */
      yychar = YYUNDEF;
      yytoken = YYSYMBOL_YYerror;
      goto yyerrlab1;
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);
  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  /* Discard the shifted token.  */
  yychar = YYEMPTY;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 2: /* M: %empty  */
#line 56 "parser.y"
               { 
    (yyval.str) = new_label(); 
    printf("%s:\n", (yyval.str)); 
}
#line 1491 "y.tab.c"
    break;

  case 9: /* VarDecl: Type IDENTIFIER SEMICOLON  */
#line 78 "parser.y"
                              {
        insertSymbol((yyvsp[-1].str), (yyvsp[-2].str), 0);
    }
#line 1499 "y.tab.c"
    break;

  case 10: /* VarDecl: IDENTIFIER NEWARRAY L_RND_BRC INT_CONST COMMA Type R_RND_BRC SEMICOLON  */
#line 81 "parser.y"
                                                                             {
        insertSymbol((yyvsp[-7].str), "Array", 0); 
        printf("%s = newArray(%s, %s)\n", (yyvsp[-7].str), (yyvsp[-4].str), (yyvsp[-2].str));
    }
#line 1508 "y.tab.c"
    break;

  case 11: /* VarDecl: IDENTIFIER IDENTIFIER NEW L_RND_BRC IDENTIFIER R_RND_BRC SEMICOLON  */
#line 85 "parser.y"
                                                                         {
        insertSymbol((yyvsp[-5].str), (yyvsp[-6].str), 0);
        printf("%s = new %s\n", (yyvsp[-5].str), (yyvsp[-2].str));
    }
#line 1517 "y.tab.c"
    break;

  case 12: /* VarDecl: IDENTIFIER IDENTIFIER SEMICOLON  */
#line 89 "parser.y"
                                      {
        insertSymbol((yyvsp[-1].str), (yyvsp[-2].str), 0);
    }
#line 1525 "y.tab.c"
    break;

  case 38: /* IfHead: IF L_RND_BRC Expr R_RND_BRC  */
#line 154 "parser.y"
                                    {
    (yyval.str) = new_label(); 
    printf("ifFalse %s goto %s\n", (yyvsp[-1].str), (yyval.str));
}
#line 1534 "y.tab.c"
    break;

  case 39: /* IfStmt: IfHead Stmt  */
#line 160 "parser.y"
                                      {
        printf("%s:\n", (yyvsp[-1].str)); 
    }
#line 1542 "y.tab.c"
    break;

  case 40: /* $@1: %empty  */
#line 163 "parser.y"
                       {
        char* L_EXIT = new_label();
        printf("goto %s\n", L_EXIT); 
        printf("%s:\n", (yyvsp[-2].str));     
        (yyvsp[-2].str) = L_EXIT;             
    }
#line 1553 "y.tab.c"
    break;

  case 41: /* IfStmt: IfHead Stmt ELSE $@1 Stmt  */
#line 168 "parser.y"
           {
        printf("%s:\n", (yyvsp[-4].str));     
    }
#line 1561 "y.tab.c"
    break;

  case 42: /* @2: %empty  */
#line 174 "parser.y"
                                     {
        char* L_EXIT = new_label();
        printf("ifFalse %s goto %s\n", (yyvsp[-1].str), L_EXIT);
        (yyval.str) = L_EXIT; // Store exit label
    }
#line 1571 "y.tab.c"
    break;

  case 43: /* WhileStmt: WHILE L_RND_BRC M Expr R_RND_BRC @2 Stmt  */
#line 178 "parser.y"
           {
        printf("goto %s\n", (yyvsp[-4].str)); // Jump to start
        printf("%s:\n", (yyvsp[-1].str)); // Print exit label
    }
#line 1580 "y.tab.c"
    break;

  case 44: /* DoWhileStmt: DO M Stmt WHILE L_RND_BRC Expr R_RND_BRC SEMICOLON  */
#line 185 "parser.y"
                                                       {
        printf("if %s goto %s\n", (yyvsp[-2].str), (yyvsp[-6].str));
    }
#line 1588 "y.tab.c"
    break;

  case 45: /* @3: %empty  */
#line 191 "parser.y"
                                                                            {
        char* L_BODY = new_label();
        char* L_EXIT = new_label();
        
        printf("ifFalse %s goto %s\n", (yyvsp[-4].str), L_EXIT);
        printf("goto %s\n", L_BODY);
        
        printf("%s:\n", (yyvsp[-2].str)); 
        printf("goto %s\n", (yyvsp[-5].str)); 
        
        printf("%s:\n", L_BODY); 
        
        (yyval.str) = L_EXIT; 
        (yyvsp[-10].str) = (yyvsp[-2].str);     
    }
#line 1608 "y.tab.c"
    break;

  case 46: /* ForStmt: FOR L_RND_BRC ExprFor SEMICOLON M ExprFor SEMICOLON M ExprFor R_RND_BRC @3 Stmt  */
#line 205 "parser.y"
           {
        printf("goto %s\n", (yyvsp[-4].str)); 
        printf("%s:\n", (yyvsp[-1].str)); 
    }
#line 1617 "y.tab.c"
    break;

  case 47: /* ExprFor: %empty  */
#line 212 "parser.y"
                { (yyval.str) = "1"; }
#line 1623 "y.tab.c"
    break;

  case 49: /* BreakStmt: BREAK SEMICOLON  */
#line 217 "parser.y"
                    { printf("goto L_BREAK\n"); }
#line 1629 "y.tab.c"
    break;

  case 50: /* ReturnStmt: RETURN ExprOpt SEMICOLON  */
#line 221 "parser.y"
                             {
        printf("return %s\n", (yyvsp[-1].str));
    }
#line 1637 "y.tab.c"
    break;

  case 51: /* ExprOpt: %empty  */
#line 227 "parser.y"
                { (yyval.str) = ""; }
#line 1643 "y.tab.c"
    break;

  case 58: /* Expr: LValue ASSIGN Expr  */
#line 237 "parser.y"
                       {
        printf("%s = %s\n", (yyvsp[-2].str), (yyvsp[0].str));
        (yyval.str) = (yyvsp[-2].str);
    }
#line 1652 "y.tab.c"
    break;

  case 59: /* Expr: Expr OR Expr  */
#line 241 "parser.y"
                   {
        (yyval.str) = new_temp();
        printf("%s = %s || %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str));
    }
#line 1661 "y.tab.c"
    break;

  case 60: /* Expr: Expr AND Expr  */
#line 245 "parser.y"
                    {
        (yyval.str) = new_temp();
        printf("%s = %s && %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str));
    }
#line 1670 "y.tab.c"
    break;

  case 61: /* Expr: Expr EQ Expr  */
#line 249 "parser.y"
                   { (yyval.str) = new_temp(); printf("%s = %s == %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1676 "y.tab.c"
    break;

  case 62: /* Expr: Expr NEQ Expr  */
#line 250 "parser.y"
                    { (yyval.str) = new_temp(); printf("%s = %s != %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1682 "y.tab.c"
    break;

  case 63: /* Expr: Expr LT Expr  */
#line 251 "parser.y"
                   { (yyval.str) = new_temp(); printf("%s = %s < %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1688 "y.tab.c"
    break;

  case 64: /* Expr: Expr LE Expr  */
#line 252 "parser.y"
                   { (yyval.str) = new_temp(); printf("%s = %s <= %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1694 "y.tab.c"
    break;

  case 65: /* Expr: Expr GT Expr  */
#line 253 "parser.y"
                   { (yyval.str) = new_temp(); printf("%s = %s > %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1700 "y.tab.c"
    break;

  case 66: /* Expr: Expr GE Expr  */
#line 254 "parser.y"
                   { (yyval.str) = new_temp(); printf("%s = %s >= %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1706 "y.tab.c"
    break;

  case 67: /* Expr: Expr PLUS Expr  */
#line 255 "parser.y"
                     {
        (yyval.str) = new_temp();
        printf("%s = %s + %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str));
    }
#line 1715 "y.tab.c"
    break;

  case 68: /* Expr: Expr MINUS Expr  */
#line 259 "parser.y"
                      { (yyval.str) = new_temp(); printf("%s = %s - %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1721 "y.tab.c"
    break;

  case 69: /* Expr: Expr MUL Expr  */
#line 260 "parser.y"
                    { (yyval.str) = new_temp(); printf("%s = %s * %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1727 "y.tab.c"
    break;

  case 70: /* Expr: Expr DIV Expr  */
#line 261 "parser.y"
                    { (yyval.str) = new_temp(); printf("%s = %s / %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1733 "y.tab.c"
    break;

  case 71: /* Expr: Expr MOD Expr  */
#line 262 "parser.y"
                    { (yyval.str) = new_temp(); printf("%s = %s %% %s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str)); }
#line 1739 "y.tab.c"
    break;

  case 72: /* Expr: NOT Expr  */
#line 263 "parser.y"
               { (yyval.str) = new_temp(); printf("%s = !%s\n", (yyval.str), (yyvsp[0].str)); }
#line 1745 "y.tab.c"
    break;

  case 73: /* Expr: MINUS Expr  */
#line 264 "parser.y"
                              { (yyval.str) = new_temp(); printf("%s = -%s\n", (yyval.str), (yyvsp[0].str)); }
#line 1751 "y.tab.c"
    break;

  case 74: /* Expr: L_RND_BRC Expr R_RND_BRC  */
#line 265 "parser.y"
                               { (yyval.str) = (yyvsp[-1].str); }
#line 1757 "y.tab.c"
    break;

  case 75: /* Expr: LValue  */
#line 266 "parser.y"
             {
        check_scope((yyvsp[0].str)); 
        (yyval.str) = (yyvsp[0].str); 
    }
#line 1766 "y.tab.c"
    break;

  case 76: /* Expr: Call  */
#line 270 "parser.y"
           { (yyval.str) = (yyvsp[0].str); }
#line 1772 "y.tab.c"
    break;

  case 77: /* Expr: Constant  */
#line 271 "parser.y"
               { (yyval.str) = (yyvsp[0].str); }
#line 1778 "y.tab.c"
    break;

  case 78: /* Expr: NEW L_RND_BRC IDENTIFIER R_RND_BRC  */
#line 272 "parser.y"
                                         {
        (yyval.str) = new_temp();
        printf("%s = new %s\n", (yyval.str), (yyvsp[-1].str));
    }
#line 1787 "y.tab.c"
    break;

  case 79: /* LValue: IDENTIFIER  */
#line 279 "parser.y"
               { (yyval.str) = (yyvsp[0].str); }
#line 1793 "y.tab.c"
    break;

  case 80: /* LValue: Expr DOT IDENTIFIER  */
#line 280 "parser.y"
                          {
        (yyval.str) = new_temp();
        printf("%s = %s.%s\n", (yyval.str), (yyvsp[-2].str), (yyvsp[0].str));
    }
#line 1802 "y.tab.c"
    break;

  case 81: /* LValue: Expr L_SQR_BRC Expr R_SQR_BRC  */
#line 284 "parser.y"
                                    {
        (yyval.str) = new_temp();
        printf("%s = %s[%s]\n", (yyval.str), (yyvsp[-3].str), (yyvsp[-1].str));
    }
#line 1811 "y.tab.c"
    break;

  case 82: /* Call: IDENTIFIER L_RND_BRC Actuals R_RND_BRC  */
#line 291 "parser.y"
                                           {
        printf("call %s, %s\n", (yyvsp[-3].str), "n");
        (yyval.str) = "call_ret"; 
    }
#line 1820 "y.tab.c"
    break;

  case 83: /* Call: Expr DOT IDENTIFIER L_RND_BRC Actuals R_RND_BRC  */
#line 295 "parser.y"
                                                      {
        (yyval.str) = "method_ret";
    }
#line 1828 "y.tab.c"
    break;

  case 86: /* ActualList: Expr  */
#line 306 "parser.y"
         { printf("param %s\n", (yyvsp[0].str)); }
#line 1834 "y.tab.c"
    break;

  case 87: /* ActualList: ActualList COMMA Expr  */
#line 307 "parser.y"
                            { printf("param %s\n", (yyvsp[0].str)); }
#line 1840 "y.tab.c"
    break;


#line 1844 "y.tab.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", YY_CAST (yysymbol_kind_t, yyr1[yyn]), &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYSYMBOL_YYEMPTY : YYTRANSLATE (yychar);
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
      yyerror (YY_("syntax error"));
    }

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;
  ++yynerrs;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  /* Pop stack until we find a state that shifts the error token.  */
  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYSYMBOL_YYerror;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYSYMBOL_YYerror)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  YY_ACCESSING_SYMBOL (yystate), yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", YY_ACCESSING_SYMBOL (yyn), yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturnlab;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturnlab;


/*-----------------------------------------------------------.
| yyexhaustedlab -- YYNOMEM (memory exhaustion) comes here.  |
`-----------------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  goto yyreturnlab;


/*----------------------------------------------------------.
| yyreturnlab -- parsing is finished, clean up and return.  |
`----------------------------------------------------------*/
yyreturnlab:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  YY_ACCESSING_SYMBOL (+*yyssp), yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif

  return yyresult;
}

#line 314 "parser.y"


char* new_temp() {
    char* t = (char*)malloc(20);
    sprintf(t, "t%d", temp_count++);
    return t;
}

char* new_label() {
    char* l = (char*)malloc(20);
    sprintf(l, "L%d", label_count++);
    return l;
}

void check_scope(char* id) {
    if(lookupSymbol(id) == NULL) {
        /* Warn or exit */
    }
}

int main() {
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error at line %d: %s\n", yylineno, s);
}
