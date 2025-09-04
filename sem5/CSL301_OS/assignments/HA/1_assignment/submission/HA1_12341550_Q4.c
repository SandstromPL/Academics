#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    //int cnt = 0;
    printf("Parent PID: %d, PPID: %d, I am Paritosh Lahre\n", getpid(), getppid());
    //cnt++;
    //printf("initial processes observed: %d\n",cnt);
    pid_t rc1 = fork();
    if (rc1 < 0) {
        perror("fork");
        exit(1);
    } 
    else if (rc1 == 0) {
        // First child
        printf("First child PID: %d, PPID: %d, I am first child\n", getpid(), getppid());
        //cnt++;
        //printf("Total processes observed(FC): %d\n",cnt);
        exit(0);
    } 

    // Parent waits for first child
    wait(NULL);

    pid_t rc2 = fork();
    if (rc2 < 0) {
        perror("fork");
        exit(1);
    } 
    else if (rc2 == 0) {
        // Second child
        printf("Second child PID: %d, PPID: %d, I am second child\n", getpid(), getppid());
        //cnt++;
        //printf("Total processes observed(SC): %d\n",cnt);
        exit(0);
    }

    // Parent waits for second child
    wait(NULL);

    // Summary (runs only in parent)
    printf("Total processes observed: 3(1 parent + 2 child)\n");

    return 0;
}
