//Question 1

#include<pthread.h>
#include<stdio.h>

int global_id = 10;

void * thread_func(void * arg){
    int thread_local;
    printf("Thread %d : local address = %p, global address = %p\n",
    *(int*)arg, (void*)&thread_local, (void*)&global_id);
}
int main(){
    pthread_t id1;
    pthread_t id2;
    int local_id = 42;
    pthread_create(&id1,NULL,thread_func,&global_id);
    pthread_create(&id2,NULL,thread_func,&local_id);
    pthread_join(id1,NULL);
    pthread_join(id2,NULL);
    printf("Main: local address = %p, global address = %p\n",
    (void*)&local_id, (void*)&global_id);
    printf("Thread finished.\n");
    return 0;
}