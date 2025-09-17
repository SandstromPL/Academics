#ifndef _PROCINFO_H_
#define _PROCINFO_H_
//TH2 -> 1
typedef unsigned long long uint64;

struct proc_info {
    int pid;
    char name[16];
    char state[16];
    uint64 sz;
};

#endif