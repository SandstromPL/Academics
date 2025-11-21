/* symboltable.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symbol.h"

Scope globalScope = {1,  NULL, NULL };
Scope* scopeStack = &globalScope;
static int scopeCounter = 1;

void enterScope(){
    Scope* newScope = (Scope*)malloc(sizeof(Scope));
    newScope->id = ++scopeCounter;
    newScope->symbols = NULL;
    newScope->next = scopeStack;
    scopeStack = newScope;
    printf("Entered new scope %d\n", newScope->id);
}

void exitScope() {
    if (scopeStack && scopeStack != &globalScope){
        Symbol* sym = scopeStack->symbols;
        while (sym) {
            Symbol* next = sym->next;
            free(sym);
            sym = next;
        }
        Scope* temp = scopeStack;
        scopeStack = scopeStack->next;
        free(temp);
        printf("Exited scope\n");
    }else{
        printf("Attempted to exit global scope — ignored\n");
    }
}

void addSymbol(const char* name, const char* type) {
    if (!scopeStack) return;
    for (Symbol* sym = scopeStack->symbols; sym; sym = sym->next) {
        if (strcmp(sym->name, name) == 0) {
            printf("Error: %s already declared in this scope (scope %d)\n",
                   name, scopeStack->id);
            return;
        }
    }
    Symbol* sym = (Symbol*)malloc(sizeof(Symbol));
    strcpy(sym->name, name);
    strcpy(sym->type, type);
    sym->next = scopeStack->symbols;
    scopeStack->symbols = sym;
    printf("Declared %s of type %s in scope %d\n", name, type, scopeStack->id);
}

Symbol* findSymbol(const char* name) {
    for (Scope* s = scopeStack; s; s = s->next)
        for (Symbol* sym = s->symbols; sym; sym = sym->next)
            if (strcmp(sym->name, name) == 0)
                return sym;
    return NULL;
}


