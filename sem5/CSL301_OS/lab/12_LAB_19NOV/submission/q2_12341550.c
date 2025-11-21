#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>
#include <grp.h>
#include <unistd.h>
#include <time.h>
#include <limits.h>

#ifndef PATH_MAX
#define PATH_MAX 4096
#endif


void print_permissions(mode_t mode) {
    char type = '-';
    if (S_ISDIR(mode)) type = 'd';
    else if (S_ISLNK(mode)) type = 'l';
    else if (S_ISCHR(mode)) type = 'c';
    else if (S_ISBLK(mode)) type = 'b';
    else if (S_ISSOCK(mode)) type = 's';
    else if (S_ISFIFO(mode)) type = 'p';

    printf("%c", type);
    printf( (mode & S_IRUSR) ? "r" : "-");
    printf( (mode & S_IWUSR) ? "w" : "-");
    printf( (mode & S_IXUSR) ? "x" : "-");
    printf( (mode & S_IRGRP) ? "r" : "-");
    printf( (mode & S_IWGRP) ? "w" : "-");
    printf( (mode & S_IXGRP) ? "x" : "-");
    printf( (mode & S_IROTH) ? "r" : "-");
    printf( (mode & S_IWOTH) ? "w" : "-");
    printf( (mode & S_IXOTH) ? "x" : "-");
}


void print_file_details(const char *path, const char *name) {
    char fullpath[PATH_MAX];

    if (snprintf(fullpath, sizeof(fullpath), "%s/%s", path, name) >= (int)sizeof(fullpath)) {
        fprintf(stderr, "Path too long: %s/%s\n", path, name);
        return;
    }

    struct stat sb;
    if (lstat(fullpath, &sb) == -1) {
        perror("stat");
        return;
    }

    print_permissions(sb.st_mode);

    struct passwd *pwd = getpwuid(sb.st_uid);
    struct group *grp = getgrgid(sb.st_gid);

    char timebuf[64];
    struct tm *tm_info = localtime(&sb.st_mtime);
    if (tm_info) {
        strftime(timebuf, sizeof(timebuf), "%b %e %H:%M", tm_info);
    } else {
        strncpy(timebuf, "??? ?? ??:??", sizeof(timebuf));
        timebuf[sizeof(timebuf) - 1] = '\0';
    }

    printf(" %2ld %s %s %8lld %s %s\n",
           (long)sb.st_nlink,
           pwd ? pwd->pw_name : "?",
           grp ? grp->gr_name : "?",
           (long long)sb.st_size,
           timebuf,
           name);

}

int main(int argc, char *argv[]) {
    int long_format = 0;
    char *dirpath = NULL;

   
    if (argc == 1) {
        dirpath = ".";
    } else if (argc == 2) {
        if (strcmp(argv[1], "-l") == 0)
            dirpath = ".";
        else
            dirpath = argv[1];
    } else if (argc == 3 && strcmp(argv[1], "-l") == 0) {
        long_format = 1;
        dirpath = argv[2];
    } else {
        fprintf(stderr, "Usage: %s [-l] [directory]\n", argv[0]);
        exit(1);
    }

    if (argc >= 2 && strcmp(argv[1], "-l") == 0)
        long_format = 1;

    DIR *dir = opendir(dirpath);
    if (!dir) {
        perror("opendir");
        return 1;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
          if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;

        if (long_format)
            print_file_details(dirpath, entry->d_name);
        else
            printf("%s\n", entry->d_name);
    }

    closedir(dir);
    return 0;
}

