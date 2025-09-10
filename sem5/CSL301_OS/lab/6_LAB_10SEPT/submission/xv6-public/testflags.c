//HA1->step7
#include "types.h"
#include "stat.h"
#include "user.h"
int main(void){
    setflag(1550);
    int retrieve = getflag();
    printf(1,"userflag value via getflag : %d\n",retrieve);

    setflag(1551);
    retrieve = getflag();
    printf(1,"userflag value via getflag : %d\n",retrieve);
    exit();
}