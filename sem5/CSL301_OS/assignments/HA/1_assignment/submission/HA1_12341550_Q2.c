#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[])
{
    fork(); // first fork
    fork(); // second fork
    wait(NULL);
    printf("PID: %d, PPID: %d\n", getpid(), getppid());
    return 0;
}
