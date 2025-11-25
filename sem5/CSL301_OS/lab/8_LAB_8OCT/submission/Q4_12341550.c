//Question 4

    #include<pthread.h>
    #include<stdio.h>
    #include<stdlib.h>

    void * compute_square(void * arg){
        int number = *(int*)arg;
        int * result = malloc(sizeof(int));
        *result = number * number;
        return result;
    }

    int main(){
        pthread_t tid;
        void * result;
        int number;
        printf("Enter the number : ");
        scanf("%d",&number);
        pthread_create(&tid,NULL,compute_square,&number);
        pthread_join(tid,&result);

        //int * value = (int*)result;
        printf("Output : %d\n",*(int*)result);

        free(result);

        return 0;
    }