#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(){
    char *p = malloc(4096);
    if(p == NULL){
        perror("malloc");
        return 1;
    }

    printf("Allocated 4KB of memory at address ; %p\n", (void*)p);
    print("Process ID : %d\n", getpid());
    printf("Press Enter to exit...\n");

    p[0] = 'a';

    getchar();
    free(p);
    return 0;
}