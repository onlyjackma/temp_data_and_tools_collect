#include<stdio.h>
#include<stdlib.h>

#define HELLO(JJJJ) static tt(){printf("jjjj=%d",JJJJ);} \
static void __attribute__((constructor)) __mmtest(void) \
{ \
	printf("hello man %d\n",JJJJ);\
}


void test2();
