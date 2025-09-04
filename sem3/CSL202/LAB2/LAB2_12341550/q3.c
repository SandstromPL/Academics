#include<stdio.h>
#include<stdlib.h>

int main(){
	
	int n1,n2,n;
	printf("Enter the size of first array : ");
	scanf("%d",&n1);
	int * A = (int *)malloc(n1 * (sizeof(int)));
	printf("Enter the elements of first array : \n");
	for(int i = 0; i < n1; i++){
		scanf("%d",&A[i]);	
	}

	printf("Enter the size of second array : ");
	scanf("%d",&n2);
	int * B = (int *)malloc(n2 * (sizeof(int)));
	printf("Enter the elements of second array : \n");
	for(int i = 0; i < n2; i++){
		scanf("%d",&B[i]);	
	}
	n = n1 + n2;
	int * ans = (int *)malloc(n * (sizeof(int)));
	int i = 0;
	int j = 0;
	int k = 0;
	while(i < n1 && j < n2){
		if(A[i] <= B[j]){
			ans[k] = A[i];
			i++;
		}else{
			ans[k] = B[j];
			j++;
		}
		k++;	
	}
	
	while(i < n1){
		ans[k] = A[i];
		i++;
		k++;	
	}
	while(j < n2){
		ans[k] = A[j];
		j++;
		k++;	
	}
	
	printf("Merged two sorted array : \n)");
	for(int z = 0; z < n; z++){
		printf("%d ",ans[z]);	
	}

	printf("\n\n");
	return 0;
}
