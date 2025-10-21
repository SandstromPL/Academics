#include<stdio.h>
#include<pthread.h>
#include<stdlib.h>
#define SEGMENT_SIZE 10
#define SIZE 100

typedef struct
{
    int *arr;
    int start;
}args;

void *partial_sum(void *arg)
{
    args *a = (args *)arg;
    int sum = 0;
    for (int i = a->start; i<a -> start + SEGMENT_SIZE; ++i)
        sum += a->arr[i];
    int *result = malloc(sizeof(int));
    *result = sum;
    return result;
}

void *total_sum(void *arg){
    int * partial_sums = (int *)arg;
    int total = 0;
    for(int i = 0; i < SEGMENT_SIZE; i++){
        total += partial_sums[i];
    }
    int * result = malloc(sizeof(int));
    *result = total;
    return result;
}

int main(){
    int arr[SIZE];
    for(int i = 0; i < SIZE; i++) arr[i] = i + 1;

    pthread_t thread[SEGMENT_SIZE];
    args segment[SEGMENT_SIZE];
    int segment_sum[SEGMENT_SIZE];

    for(int i = 0; i < 10; i++){
        segment[i].arr = arr;
        segment[i].start = i * SEGMENT_SIZE;
        pthread_create(&thread[i],NULL,partial_sum,&segment[i]);
    }

    
    for(int i = 0; i < SEGMENT_SIZE; i++){
        void * result;
        pthread_join(thread[i],&result);
        segment_sum[i] = *((int *)result);
        printf("Thread %d partial sum : %d\n",i + 1,*((int *)result));
        free(result);
    }
    
    pthread_t master_sum;
    void *total;

    pthread_create(&master_sum,NULL,total_sum,segment_sum);
    pthread_join(master_sum,&total);

    printf("Total sum : %d\n",*((int *)total));

    double average = (double)*((int *)total) / SIZE;
    printf("Average : %f\n",average);
}
