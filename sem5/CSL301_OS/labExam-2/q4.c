#include<stdio.h>
#include<dirent.h>
#include<string.h>
#include<sys/stat.h>
#include<stdlib.h>
#include<unistd.h>

void explore(const char *path,int depth,int level){
    if(level > depth)
    return;
    DIR *d = opendir(path);
    if(!d){
        for(int i = 0; i < level * 4; i++)
        printf(" ");
        printf("%s [ACCESS DENIED]\n", path);
        return;
    }

    struct dirent *de;
    char newpath[512];
    while((de = readdir(d)) != NULL){
        if(strcmp(de->d_name, ".") == 0 || strcmp(de->d_name, "..") == 0)
            continue;
        for(int i = 0; i < level * 4; i++)
            printf(" ");
        snprintf(newpath, sizeof(newpath), "%s/%s", path, de->d_name);
        struct stat st;
        lstat(newpath, &st);
        printf("%s", de->d_name);
        if(S_ISDIR(st.st_mode)){
            printf(" [DIR]\n");
            explore(newpath, depth, level + 1);
        } else {
            printf("\n");
        }
    }
    closedir(d);
}

int main(int arc, char *argv[]){
    if(arc != 3){
        printf("Usage: %s <directory> <depth>\n", argv[0]);
        return 1;
    }
    int depth = atoi(argv[2]);
    printf("%s\n", argv[1]);
    if(depth > 0)
    explore(argv[1], depth, 1);
    return 0;
}