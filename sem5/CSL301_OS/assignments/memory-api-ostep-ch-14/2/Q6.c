#include<stdio.h>
#include<stdlib.h>



int main(){

	int * data = (int *)malloc(100);
	//printf("val before ; %d\n",data[69]);
	free(data);
	printf("val : %d\n",data[69]);
	return 0;

}
