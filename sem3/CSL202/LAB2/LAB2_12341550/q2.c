#include<stdio.h>
#include<stdlib.h>

int main(){
	
	int n,position;
	printf("Enter the size of arry : ");
	scanf("%d",&n);
	int * arr = (int *)malloc(n * (sizeof(int)));
	printf("Enter the elements of array :\n");
	for (int i = 0; i < n; i++){
		scanf("%d",&arr[i]);	
	}

	printf("Enter the postion : ");
	scanf("%d",&position);

	int * ans = (int *)malloc((n - 1) * (sizeof(int)));
	int i;
	for(i = 0; i < position - 1; i++){
		ans[i] = arr[i];	
	}
	
	int j = i + 1;
	while(i < n - 1){
		ans[i] = arr[j];
		i++;
		j++;	
	}
	
	printf("New array : \n");
	for(int k = 0; k < n - 1; k++){
		printf("%d ",ans[k]);	
	}
	return 0;
	
}
