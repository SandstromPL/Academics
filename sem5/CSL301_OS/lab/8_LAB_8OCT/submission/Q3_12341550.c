//Question 3

#include<pthread.h>
#include<stdio.h>

int global_var = 10;

void * thread_func(void * arg){
    int id = *(int*)arg;
    global_var += 1000000;
    printf("Thread ID : %d , golbal var : %d\n",id,global_var);
    return NULL;
}

int main(){
    pthread_t arr[10] = {1,2,3,4,5,6,7,8,9,10};
    int id[10] = {1,2,3,4,5,6,7,8,9,10};
    for(int i = 0; i < 10; i++){
        pthread_create(&arr[i],NULL,thread_func,&id[i]);
    }
    for(int i = 0; i < 10; i++){
        pthread_join(arr[i],NULL);
    }
    printf("All threads completed.\n");
    return 0;
}