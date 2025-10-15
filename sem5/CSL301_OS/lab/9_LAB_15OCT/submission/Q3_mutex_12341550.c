        #include <stdio.h>
        #include <pthread.h>

        int counter = 0;
        pthread_mutex_t lock;

        void* increment(void* arg) 
        {
        for(int i = 0; i < 2; i++) 
        {
            pthread_mutex_lock(&lock);
            counter = counter + 50000;
            printf("Thread %ld: Counter = %d\n", (long)arg, counter);
            pthread_mutex_unlock(&lock);
        }
        return NULL;
        }

        int main() 
        {
        pthread_t arr_t[10];
        
        pthread_mutex_init(&lock, NULL);
        
        for(int i = 0; i < 10; i++){
            pthread_create(&arr_t[i], NULL, increment, (void*)i+1);
        }
        /* pthread_create(&t1, NULL, increment, (void*)1);
        pthread_create(&t2, NULL, increment, (void*)2); */
        
        for(int i = 0; i < 10; i++){
            pthread_join(arr_t[i],NULL);
        }
        /* pthread_join(t1, NULL);
        pthread_join(t2, NULL); */
        
        return 0;
        }
