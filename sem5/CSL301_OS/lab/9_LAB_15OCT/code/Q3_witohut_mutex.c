        #include <stdio.h>
        #include <pthread.h>

        int counter = 0;

        void* increment(void* arg) 
        {
        for(int i = 0; i < 2; i++) 
        {
            counter = counter + 50000;
            printf("Thread %ld: Counter = %d\n", (long)arg, counter);
        }
        return NULL;
        }

        int main() 
        {
        pthread_t arr_t[10];
        
        
        for(int i = 0; i < 10; i++){
            pthread_create(&arr_t[i], NULL, increment, (void*)i+1);
        }
        
        for(int i = 0; i < 10; i++){
            pthread_join(arr_t[i],NULL);
        }
        
        return 0;
        }
