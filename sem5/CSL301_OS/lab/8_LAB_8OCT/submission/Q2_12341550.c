//Question 2

#include<pthread.h>
#include<stdio.h>

void * print_id(void * arg){
    int id = *(int*)arg;
    printf("Thread ID : %d is running\n",id);
    return NULL;
}

int main(){
    pthread_t arr[10] = {1,2,3,4,5,6,7,8,9,10};
    int id[10] = {1,2,3,4,5,6,7,8,9,10};
    for(int i = 0; i < 10; i++){
        pthread_create(&arr[i],NULL,print_id,&id[i]);
    }
    for(int i = 0; i < 10; i++){
        pthread_join(arr[i],NULL);
    }
    printf("All threads completed.\n");
    return 0;
}