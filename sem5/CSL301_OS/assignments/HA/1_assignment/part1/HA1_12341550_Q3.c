#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>

int main(void) {
    int fd = open("./3_output.txt", O_CREAT | O_WRONLY | O_APPEND, 0644);
    if (fd < 0) {
        perror("open");
        exit(1);
    }

    pid_t rc = fork();

    if (rc < 0) {
        perror("fork");
        exit(1);
    } 
    else if (rc == 0) {
        dprintf(fd, "12341550\n");
        printf("Child: wrote roll number to file\n");
    } 
    else {
        wait(NULL);
        dprintf(fd, "Paritosh Lahre\n");
        printf("Parent: wrote name to file\n");
    }

    close(fd);
    return 0;
}
