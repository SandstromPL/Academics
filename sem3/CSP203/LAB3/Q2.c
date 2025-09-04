#include<stdio.h>
#include<stdlib.h>

int main(){
	int n;
	printf("Enter the size n * n matrix : ");
	scanf("%d",&n);
	int (*A)[n][n] = malloc(sizeof(*A));
	int (*B)[n][n] = malloc(sizeof(*B));
	int (*P)[n][n] = malloc(sizeof(*P));
	printf("Enter the elements of matrix A : \n");
	for(int i = 0; i < n; i++){
		for(int j = 0; j < n; j++){
			int temp;
			scanf("%d",&temp);
			(*A)[i][j] = temp;
		}
	}
	printf("Enter the elements of matrix B : \n");
	for(int i = 0; i < n; i++){
                for(int j = 0; j < n; j++){
                        int temp;
                        scanf("%d",&temp);
                        (*B)[i][j] = temp;
                }
        }
	for(int i = 0; i < n; i++){
		//int cnt = 0;
		for(int j = 0; j < n; j++){
			int temp = (*A)[i][j] * (*B)[i][j] + (*A)[i][j + 1] * (*B)[i + 1][j] + (*A)[i][j + 2] * (*B)[i + 2][j] ;
			(*P)[i][j] = temp;
		}
	}


}
