// HA3->step5
#include "types.h"
#include "stat.h"
#include "user.h"
int main(int argc, char *argv[])
{
    int pid1, pid2, pid3, pid4, pid5;
    printf(1, " Starting priority scheduling test ...\n ");

    pid1 = fork();
    if (pid1 == 0)
    {
        setpriority(10);
        printf(1, " Child 1 (pid %d) with priority (10) started .\n ",
               getpid());
        for (int i = 0; i < 50000000; i++)
        {
        } // Busy loop
        printf(1, " Child 1 finished .\n ");
        exit();
    }

    pid2 = fork();
    if (pid2 == 0)
    {
        setpriority(50);
        printf(1, " Child 2 (pid %d) with priority (50) started .\n ",
               getpid());
        for (int i = 0; i < 50000000; i++)
        {
        } // Busy loop
        printf(1, " Child 2 finished .\n ");
        exit();
    }

    pid3 = fork();
    if (pid3 == 0)
    {
        setpriority(70); // Low priority
        printf(1, " Child 3 (pid %d) with priority (70) started .\n ",
               getpid());
        for (int i = 0; i < 50000000; i++)
        {
        } // Busy loop
        printf(1, " Child 3 finished .\n ");
        exit();
    }

    pid4 = fork();
    if (pid4 == 0)
    {
        setpriority(30); // Low priority
        printf(1, " Child 4 (pid %d) with priority (30) started .\n ",
               getpid());
        for (int i = 0; i < 50000000; i++)
        {
        } // Busy loop
        printf(1, " Child 4 finished .\n ");
        exit();
    }

    pid5 = fork();
    if (pid5 == 0)
    {
        setpriority(5); // Low priority
        printf(1, " Child 5 (pid %d) with priority (5) started .\n ",
               getpid());
        for (int i = 0; i < 50000000; i++)
        {
        } // Busy loop
        printf(1, " Child 5 finished .\n ");
        exit();
    }
    wait();
    wait();
    wait();
    wait();
    wait();
    printf(1, " Priority scheduling test complete .\n ");
    exit();
}