#include <err.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/types.h>
#include <unistd.h>


#define MAX_BINARY_SIZE (10 * 1024 * 1024)



void readall(int8_t *buf, size_t size)
{
    int8_t *pos;
    size_t rbytes, total_rbytes = 0;
    
    pos = buf;

    while (total_rbytes < size) {
        rbytes = read(0, pos, size - total_rbytes);
        if (rbytes <= 0)
            err(1, "failed to recvall");

        total_rbytes += rbytes;
        pos += rbytes;
    }
}

int main()
{
    int fd;
    uint32_t size;
    int8_t *data;

    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    
    alarm(120);

    puts("Hello! This friendly is not intended for you to hack it, it just loads your binary onto the remote server");
    puts("First, send length of binary 32-bit LE integer, then the ELF file itself:");

    if (read(0, &size, sizeof(size)) != sizeof(size)) 
        err(1, "failed to read size");

    if (size > MAX_BINARY_SIZE)
        err(1, "size is too big");

    data = calloc(1, size);
    if (data == NULL)
        err(1, "oom");

    readall(data, size);

    fd = open("solution", O_WRONLY | O_CREAT | O_EXCL, 0700);
    if (fd < 0)
        err(1, "failed to open file");

    if (write(fd, data, size) != size)
        err(1, "failed to write to binary file. something is wrong");
    close(fd);

    char *args[] = {
        "solution",
        NULL,
    };

    execve("solution", args, NULL);
    err(1, "failed to start binary");
    return 0;
}
