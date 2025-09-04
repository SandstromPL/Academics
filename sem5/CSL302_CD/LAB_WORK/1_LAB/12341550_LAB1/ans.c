#include<stdio.h>
#include<stdbool.h>
#include<string.h>
#include<stdlib.h>
#include<ctype.h>

bool isKeyWord(char * word){
    if( strcmp(word,"echo") == 0 || 
        strcmp(word,"foreach") == 0 || 
        strcmp(word,"read") == 0){
            return 1;
    }
    return 0;
}

bool isIdentifier(char * word){
    int l = strlen(word);
    if(l < 3) return 0;

    if(word[0] != '_' || !isdigit(word[l-1])) return 0;

    for(int i = 1; i < l - 1; i++){
        if(!islower(word[i])) return 0;
    }

    return 1;
}

int main (){
    FILE * f;
    char word[1000];

    f = fopen("input.txt","r");
    if(f == NULL){
        printf("File is empty.\n");
        fclose(f);
        return 1;
    }

    //keywords
    printf("keywords are : \n");
    while(fscanf(f,"%s",word) != EOF){
        if(isKeyWord(word)){
            printf("%s\n",word);
        }
    }
    printf("\n");
    //identifiers
    rewind(f);
    printf("identifiers are : \n");
    while(fscanf(f,"%s",word) != EOF){
        if(!isKeyWord(word) && isIdentifier(word)){
            printf("%s\n",word);
        }
    }
    fclose(f);
    return 0;

}