// Question 5 (Updated for n threads)

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#define INT_MIN -1000000000
#define INT_MAX 1000000000
int arr[1000];
int n;
int segment_size;

void *compute_min(void *arg)
{
    int start_index = (*(int *)arg);
    int *min = malloc(sizeof(int));
    min = INT_MAX;
    for (int i = start_index; i < start_index + segment_size; i++)
    {
        if (arr[i] < min)
            min = arr[i];
    }
    return min;
}

void *compute_max(void *arg)
{
    int start_index = (*(int *)arg);
    int *max = malloc(sizeof(int));
    max = INT_MIN;
    for (int i = start_index; i < start_index + segment_size; i++)
    {
        if (arr[i] > max)
            max = arr[i];
    }

    return max;
}

int main()
{

    printf("Enter number of threads : ");
    scanf("%d", &n);

    for (int i = 0; i < 1000; i++)
    {
        arr[i] = i + 1;
    }

    segment_size = 1000 / n;

    pthread_t tid[n];
    void *res_mini[n];
    void *res_maxi[n];
    int *mini = malloc(n * sizeof(int *));
    int *maxi = malloc(n * sizeof(int *));

    for (int i = 0; i < n; i++)
    {
        pthread_create(&tid[i], NULL, compute_min, &mini[i]);
        pthread_create(&tid[i], NULL, compute_max, &maxi[i]);
    }

    for (int i = 0; i < n; i++)
    {
        pthread_join(tid[i], &res_mini[i]);
        pthread_join(tid[i], &res_maxi[i]);
    }

    int final_min = INT_MAX;
    for (int i = 0; i < n; i++)
    {
        int *val = (int *)res_mini[i];
        if (*val < final_min)
            final_min = *val;
        free(val);
    }

    int final_max = INT_MIN;
    for (int i = 0; i < n; i++)
    {
        int *val = (int *)res_mini[i];
        if (*val > final_max)
            final_max = *val;
        free(val);
    }

    printf("Final minimum value : %d, Final maximum value : %d.", final_min, final_max);

    free(mini);
    free(maxi);
    return 0;
}
