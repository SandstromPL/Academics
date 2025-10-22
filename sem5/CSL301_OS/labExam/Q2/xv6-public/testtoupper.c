//Q2 - part f
#include "types.h"
#include "stat.h"
#include "user.h"

int main(void){
    char stringArray[32] = "Paritosh Lahre";
    printf(1,"Before : %s\n", stringArray);
    toupper(stringArray, strlen(stringArray));
    printf(1, "After : %s\n", stringArray);
    exit();
}