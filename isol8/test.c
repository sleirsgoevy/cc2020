asm("xxx:\nmov 8(%rsp), %rax\nsyscall\nret");

typedef unsigned long long ULL;

ULL xxx(ULL, ULL, ULL, ULL, ULL, ULL, int);

void writeall(int fd, char* buf, int cnt)
{
    while(cnt)
    {
        int chk = xxx(fd, (ULL)buf, cnt, 0, 0, 0, 1);
        buf += chk;
        cnt -= chk;
    }
}

void readall(int fd, char* buf, int cnt)
{
    while(cnt)
    {
        int chk = xxx(fd, (ULL)buf, cnt, 0, 0, 0, 0);
        buf += chk;
        cnt -= chk;
    }
}

void _start()
{
    char buf[184];
    ULL* args = (ULL*)buf;
    for(;;)
    {
        readall(0, buf, 184);
        for(int i = 0; i < 6; i++)
            if(args[i] == 0xdeadbeef)
                args[i] = (ULL)(buf + 56);
        args[6] = xxx(args[0], args[1], args[2], args[3], args[4], args[5], args[6]);
        writeall(1, buf, 184);
    }
}
