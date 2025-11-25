#include <stdio.h>
#include <pthread.h>

int counter = 0;
int critical_limit = 100;
void *decrement(void *arg)
{

        if(critical_limit > 50){
            critical_limit -= 10;
        }
        printf("Thread %ld decremented. New value: %d\n", (long)arg, critical_limit);   
    return NULL;
}

int main()
{
    pthread_t arr_t[4];

    printf("Initial value: 100\n");
    for (int i = 0; i < 4; i++)
    {
        pthread_create(&arr_t[i], NULL, decrement, (void *)i + 1);
    }

    for (int i = 0; i < 4; i++)
    {
        pthread_join(arr_t[i], NULL);
    }

    printf("Final Value (Unsafe): %d\n",critical_limit);
    return 0;
}
