#ifndef SYMBOLTABLE_H
#define SYMBOLTABLE_H

#define MAX_ID_LEN 50
#define TABLE_SIZE 100

typedef struct Symbol {
    char name[MAX_ID_LEN];
    char type[20];
    int scope;
    struct Symbol* next;
} Symbol;

extern Symbol* symbolTable[TABLE_SIZE];

unsigned int hash(char *str);
void insertSymbol(char* name, char* type, int scope);
Symbol* lookupSymbol(char* name);

#endif
