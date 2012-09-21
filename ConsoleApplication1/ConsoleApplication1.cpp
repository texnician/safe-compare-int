// ConsoleApplication1.cpp : 定义控制台应用程序的入口点。
//

#include <stdio.h>
#include <string>
#include <stdint.h>
#include "intcmp.h"

int main(int argc, char* argv[])
{
  printf("%d\n", IntLt(1, 2));
  printf("%d\n", IntGt(2, 1));
  printf("%d\n", IntEq(2, 2));
  int n = -1;
  printf("%d\n", IntLt(n, (unsigned int)1));
  printf("%d\n", IntLt(n, (int)1));
  uint64_t i64 = 1;
  int32_t i32 = -2;
  int16_t i16 = -9;
  printf("%d\n", IntGt(i64, i32));
  printf("%d\n", IntLt(i16, i32));
  size_t a = 100;
  ssize_t b = -9;
  int c = 17;
  printf("%d\n", IntGt(a, b));
  printf("%d\n", IntLt(b, a));
  printf("%d\n", IntGe(b, i16));
  printf("%d\n", IntLe(b, i16));
  printf("%d\n", IntLe(b, 'a'));
  printf("%d\n", IntGt(c, i64));
  printf("%d\n", IntGt(uint32_t(18), c));
  return 0;
}
