// Question 5 (Updated for n threads)

    #include <pthread.h>
    #include <stdio.h>
    #include <stdlib.h>

    void * compute_square(void * arg){
        int number = *(int*)arg;
        int * result = malloc(sizeof(int));
        *result = number * number;
        return result;
    }

    int main(){
        int n;
        printf("Enter number of threads : ");
        scanf("%d", &n);

        pthread_t tid[n];
        void * res[n];
        int * nums = malloc(n * sizeof(int));

        for(int i = 0; i < n; i++){
            printf("Enter the number : ");
            scanf("%d", &nums[i]);
            pthread_create(&tid[i], NULL, compute_square, &nums[i]);
        }

        for(int i = 0; i < n; i++){
            pthread_join(tid[i], &res[i]);  
        }

        for(int i = 0; i < n; i++){
            int * val = (int*)res[i];
            printf("Thread %d returned %d\n", nums[i], *val);
            free(val);
        }

        free(nums);
        return 0;
    }
