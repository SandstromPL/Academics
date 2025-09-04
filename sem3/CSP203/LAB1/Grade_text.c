#include<stdio.h>
#include<stdlib.h>

int main(){

	FILE * Rf,* Wf;
	char ch;
	Rf = fopen("Grade.c","r");
	if(Rf == NULL){
		printf("File is empty. \n");
		return 1;
	}
	
	Wf = fopen("read.txt","w");
	if(Wf == NULL){
		printf("Error opening source file .\n");
		fclose(Rf);
		return 1;
	}
	
	while((ch = fgetc(Rf)) != EOF){
		fputc(ch, Wf);
	}
	
	fclose(Rf);
	fclose(Wf);
	
	printf("File copied successfully.\n\n");
	return 0;
}
