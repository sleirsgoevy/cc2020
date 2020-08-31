asm("xxx:\nmov 8(%rsp), %rax\nsyscall\nret");

typedef unsigned long long ULL;

ULL xxx(ULL, ULL, ULL, ULL, ULL, ULL, int);

void _start()
{
    char x[] = "/bin/sh";
    char* y[] = {x, 0};
    xxx(x, y, 0, 0, 0, 0, 59);
}
