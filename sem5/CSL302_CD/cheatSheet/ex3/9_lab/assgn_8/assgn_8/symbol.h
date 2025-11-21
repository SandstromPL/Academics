/* symboltable.h */
#ifndef SYMBOLTABLE_H
#define SYMBOLTABLE_H

#define MAX_ID_LEN 50
#define TABLE_SIZE 100

typedef struct Symbol {
    char name[MAX_ID_LEN];
    char type[20];   // int, float, char, etc.
    struct Symbol* next;
} Symbol;

typedef struct Scope {
    int id;
    Symbol* symbols;
    struct Scope* next;
} Scope;

extern Scope* scopeStack;

Symbol* symbolTable[TABLE_SIZE];

//unsigned int hash(char *str);
void enterScope();
void exitScope();
void addSymbol(const char* name, const char* type);
Symbol* findSymbol(const char* name);

#endif

