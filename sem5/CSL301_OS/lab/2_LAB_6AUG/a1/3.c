#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    pid_t rc = fork();

    if (rc < 0) {
        fprintf(stderr, "fork failed\n");
        exit(1);
    } else if (rc == 0) {
        
        //execl("/bin/ls", "ls", NULL);
        char *args[] = {"/bin/ls", NULL};
        execv("/bin/ls", args);
        
        fprintf(stderr, "execl failed\n");
        exit(1);
    } else {
        int wc = wait(NULL);
        printf("Parent finished\n");
    }

    return 0;
}

