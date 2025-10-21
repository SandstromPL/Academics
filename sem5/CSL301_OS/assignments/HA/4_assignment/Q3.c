#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <time.h>
#include <limits.h>

#define N 10
#define SEGMENT_SIZE 10
#define SIZE (N * SEGMENT_SIZE)

typedef struct
{
    int *arr;
    int start;
} args;

void *partial_max(void *arg)
{
    args *a = (args *)arg;
    int max_val = INT_MIN;

    for (int i = a->start; i < a->start + SEGMENT_SIZE; ++i)
    {
        if (a->arr[i] > max_val)
        {
            max_val = a->arr[i];
        }
    }

    int *result = malloc(sizeof(int));
    *result = max_val;
    return result;
}

void *overall_max(void *arg)
{
    int *partial_maxima = (int *)arg;
    int total_max = INT_MIN;

    for (int i = 0; i < N; i++)
    {
        if (partial_maxima[i] > total_max)
        {
            total_max = partial_maxima[i];
        }
    }

    int *result = malloc(sizeof(int));
    *result = total_max;
    return result;
}

int main()
{
    srand(time(NULL));

    int arr[SIZE];
    printf("Array: [");
    for (int i = 0; i < SIZE; i++)
    {
        arr[i] = rand() % 100;
        printf("%d%s", arr[i], (i == SIZE - 1) ? "" : ", ");
    }
    printf("]\n\n");

    pthread_t thread[N];
    args segment[N];
    int segment_max[N];

    for (int i = 0; i < N; i++)
    {
        segment[i].arr = arr;
        segment[i].start = i * SEGMENT_SIZE;
        pthread_create(&thread[i], NULL, partial_max, &segment[i]);
    }

    for (int i = 0; i < N; i++)
    {
        void *result;
        pthread_join(thread[i], &result);
        
        segment_max[i] = *((int *)result);
        
        printf("Thread %d max: %d\n", i + 1, *((int *)result)); 
        
        free(result);
    }

    pthread_t master_max;
    void *overall;

    pthread_create(&master_max, NULL, overall_max, segment_max);
    pthread_join(master_max, &overall);

    printf("\nOverall max: %d\n", *((int *)overall));

    free(overall);
    
    return 0;
}