#include <stdio.h>
#include <stdlib.h>
int fib(int n){
if(n<=1){
return 1;}
int a=0;
int b=1;
int c;
for(int i=2;i<=n;i++){
c=a+b;
a=b;
b=c;}
return c;
}
int main(int argc,char *argv[]){
if(argc!=2){
printf("usage: %s <n>",argv[0]);
return 1;}
int n=atoi(argv[1]);
if(n<0){
printf("enter valid input");
return 1;
}
printf("%d th term of fib series is %d",n,fib(n));
return 0;}
