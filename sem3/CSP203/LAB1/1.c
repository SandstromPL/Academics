#include<stdio.h>

int main(){
	
	char grade;
	printf("Enter grade of student : ");
	scanf("%c",&grade);
	if(grade == 'A'){
		printf("Your performance is excellent.\n");
	}else if(grade == 'B'){
		printf("Your performance is good.\n");
	}else if(grade == 'C'){
		printf("Your performance is fair.\n");
	}else if(grade == 'D'){
		printf("Your performance is poor.\n");
	}else if(grade == 'E'){
		printf("Your grade is not complete.\n");
	}else if(grade == 'F'){
		printf("You are failed.\n");
	}else{
		printf("Invalid character.\n");
	}
	return 0;
}
