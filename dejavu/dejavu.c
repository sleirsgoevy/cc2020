#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <pthread.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/stat.h>

const char *storage_prefix = "./storage/";


int verify_path(char *path)
{
    if (strstr(path, ".."))
        return 0;

    return 1;
}


int do_readfile(char *filename) {
    int fd;
    char *fullname;
    mode_t mode;
    struct stat st;

    if (strlen(filename) > 4096 - strlen(storage_prefix) - 1) {
        return EXIT_FAILURE;
    }

    int len = strlen(storage_prefix) + strlen(filename);
    fullname = calloc(1, len + 1);
    if (fullname == NULL) {
        return -ENOMEM;
    }

    strncpy(fullname, storage_prefix, len);
    strncat(fullname, filename, len);

    // protect against directory traversal attack
    if (!verify_path(fullname)) {
        puts("Sorry, can't read that file! You are trying to hack me!");
        return EXIT_FAILURE;
    }

    // protect against symlink attack
    if (lstat(fullname, &st) != 0) {
        puts("Failed to stat a file");
        return EXIT_FAILURE;
    }

    mode = st.st_mode;
    if (S_ISLNK(mode)) {
        puts("File is a symbolic link! We are getting hacked!");
        return EXIT_FAILURE;
    }

    // get real uid of file owner
    uid_t realuid = getuid();
    if (st.st_uid != realuid) {
        puts("We are not file owner! Bailing out!");
        return EXIT_FAILURE;
    }

    // Seems we are ok now, they will never read the flag! >:D
    fd = open(fullname, O_RDONLY);
    if (fd < 0){
        puts("failed to open file");
        return EXIT_FAILURE;
    }
    char *buf = alloca(st.st_size);
    if (read(fd, buf, st.st_size) <= 0) {
        puts("failed to read file contents");
        return EXIT_FAILURE;
    }

    return write(1, buf, st.st_size) == st.st_size;
}

int do_writefile(char *filename, char *string) {
    int fd;
    int slen = strlen(string);
    char *fullname;

    if (strlen(filename) > 4096 - strlen(storage_prefix) - 1) {
        return EXIT_FAILURE;
    }

    int len = strlen(storage_prefix) + strlen(filename);
    fullname = calloc(1, len + 1);
    if (fullname == NULL) {
        return -ENOMEM;
    }

    strncpy(fullname, storage_prefix, len);
    strncat(fullname, filename, len);

    // protect against directory traversal attack
    if (!verify_path(fullname)) {
        puts("Sorry, can't read that file! You are trying to hack me!");
        return EXIT_FAILURE;
    }

    // do_writefile is so much less hardened...

    // drop privileges to real uid
    seteuid(getuid());
    setegid(getgid());
    fd = open(fullname, O_WRONLY | O_CREAT | O_EXCL, 0744);
    if (fd < 0) {
        puts("failed to open file");
        return EXIT_FAILURE;
    }

    if (write(fd, string, slen) != slen) { 
        puts("failed to write file");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}


void usage(char *argv_0)
{
    printf("Usage: %s\n\treadfile <filename>\n\twritefile <filename> <string_to_write>\n", argv_0);
}

int main(int argc, char *argv[])
{
    if (argc < 3) {
        usage(argv[0]);
        return 1;
    }
    
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char *operation = argv[1];
    char *filename = argv[2];
    

    if (!strcmp(operation, "readfile")) {
        return do_readfile(filename);
    }

    if (!strcmp(operation, "writefile")) {
        if (argc < 4) {
            usage(argv[0]);
            return EXIT_FAILURE;
        }

        return do_writefile(filename, argv[3]);
    }

    puts("unknown opration!");
    return EXIT_FAILURE;
}
