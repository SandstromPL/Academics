#include<stdio.h>

void fib(int n){
	int c,a = 0,b = 1,i = 1;
	while(i <= n){
		if(i == 1){
			printf("0 ");
			i++;
		}else if(i == 2){
			printf("1 ");
			i++;
		}else{
			c = a + b;
			printf("%d ",c);
			a = b;
			b = c;
			i++;
		}
	}
	printf("\n");
}

int main(){
	int n;
	printf("Enter the number : ");
	scanf("%d",&n);
	fib(n);
}
