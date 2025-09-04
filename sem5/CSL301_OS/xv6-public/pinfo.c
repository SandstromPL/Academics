//HA2
#include "types.h"
#include "stat.h"
#include "user.h"
#include "procinfo.h"

int main(int arg, char *argv[]){
    
    struct proc_info info;
    int pid;
    if(arg < 2){
        printf(2,"Usage: pinfo <pi>\n");
        exit();
    }

    pid = atoi(argv[1]);

    if(get_proc_info(pid, &info) < 0){
        printf(2,"Error: Process with PID %d not found.\n",pid);
        exit();
    }else{
        printf(1, "PID: %d\n",info.pid);
        printf(1, "Name: %s\n",info.name);
        printf(1, "State: %s\n",info.state);
        printf(1, "Memory Size: %d\n",info.sz);
    }

    exit();
}
