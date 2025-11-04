#include "types.h"
#include "stat.h"
#include "user.h"

int main(void)
{
  printf(1, "Code/data: %p\n", (void*) memlayout());
  printf(1, "Heap: %p\n", malloc(1));
  int x = 0;
  printf(1, "Stack: %p\n", (void*) &x);
  return 0;
}