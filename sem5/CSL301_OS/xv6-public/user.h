#include "procinfo.h"
#include "types.h"
struct stat;
struct rtcdate;
//LAB4-TA7-gmeet
struct procstats
{
    int count;
    int ticks;
};

// system calls
int fork(void);
int exit(void) __attribute__((noreturn));
int wait(void);
int pipe(int*);
int write(int, const void*, int);
int read(int, void*, int);
int close(int);
int kill(int);
int exec(char*, char**);
int open(const char*, int);
int mknod(const char*, short, short);
int unlink(const char*);
int fstat(int fd, struct stat*);
int link(const char*, const char*);
int mkdir(const char*);
int chdir(const char*);
int dup(int);
int getpid(void);
char* sbrk(int);
int sleep(int);
int uptime(void);
int strrev(char*,int);  //CA1->step4
int setflag(int);   //HA1->step5
int getflag(void);   //HA1->step5
int getstats(int * stats_array);    //LAB4-TA7-gmeet
int get_proc_info(int,struct proc_info*);   //HA2
int numvp(void);    //LAB5-CA4-step2
int numpp(void);    //LAB5-CA4-step2
int getptsize(void);    //LAB5-CA4-step2
int setpriority(int);  //HA3->step4

// ulib.c
int stat(const char*, struct stat*);
char* strcpy(char*, const char*);
void *memmove(void*, const void*, int);
char* strchr(const char*, char c);
int strcmp(const char*, const char*);
void printf(int, const char*, ...);
char* gets(char*, int max);
uint strlen(const char*);
void* memset(void*, int, uint);
void* malloc(uint);
void free(void*);
int atoi(const char*);

