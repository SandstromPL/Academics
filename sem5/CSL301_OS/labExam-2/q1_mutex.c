#include <stdio.h>
#include <pthread.h>

int critical_limit = 100;
pthread_mutex_t lock;
void *increment(void *arg)
{

    pthread_mutex_lock(&lock);
    if (critical_limit > 50)
    {
        critical_limit -= 10;
    }
    printf("Thread %ld decremented. New value: %d\n", (long)arg, critical_limit);
    pthread_mutex_unlock(&lock);
    return NULL;
}

int main()
{
    pthread_t arr_t[4];
    pthread_mutex_init(&lock, NULL);

    printf("Initial value: 100\n");
    for (int i = 0; i < 4; i++)
    {
        pthread_create(&arr_t[i], NULL, increment, (void *)i + 1);
    }

    for (int i = 0; i < 4; i++)
    {
        pthread_join(arr_t[i], NULL);
    }

    printf("Final Value (safe): %d\n",critical_limit);

    return 0;
}
