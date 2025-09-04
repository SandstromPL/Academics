#include<stdio.h>

int main(){

    FILE * file;
    char target[100];
    char filename[100];
    char line[1000];
    int linenum = 1;
    printf("Enter filename : ");
    scanf("%s",filename);
    printf("Enter target string : ");
    scanf("%s",target);
    file = fopen(filename,"r");
    if(file == NULL)
        printf("Error opening file\n");
    while(fgets(line,sizeof(line),file)){
        int i = 0,j = 0;
        while(line[i] != '\0'){
            if(line[i] == target[j]){
                j++;
            
                if(target[j] == '\0'){
                    printf("%d : %s",linenum,line);
                    break;
                }
            }else{
                j = 0;
            }
            i++;
        }
        linenum++;
    }
    fclose(file);
}