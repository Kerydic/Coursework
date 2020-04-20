#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <regex.h>
#include <fcntl.h>
#include <unistd.h>

char *regular(char *path_0){
	char *path = malloc(16);
	char *path_1 = malloc(16);
	strcpy(path,path_0);
    int count = 0;
    for(int i = 0;i < sizeof(path);i++){
        count++;
        if(path[i]=='*'){
            count ++;
            for(int j = sizeof(path)+count;j >= i;j--){
                path[j+1] = path[j];
            }
            path[i] = '.';
            i++;
        }
    }
    strcpy(path_1,path);
    return path_1;
}

int judge_byname(char *path, char *file_name){
    int status;
    int cflags = REG_EXTENDED;
    regmatch_t pmatch[1];
    const size_t nmatch = 1;
    regex_t reg;
    const char * pattern = regular(file_name);
    regcomp(&reg, pattern, cflags);


    status = regexec(&reg, path, nmatch, pmatch, 0);
    if(status == REG_NOMATCH){
        return 1;
        // not match
    }else if(status == 0){
        // match
        return 0;
    }
}

int main(int argc, char *argv[]){
    /*char *path = "test.c";
    char *file_name = argv[1];

    if(judge_byname(path,file_name) == 1){
    	printf("1");
    }else if(judge_byname(path,file_name) == 0){
    	printf("0");
    }*/
    char *path = "get*()";
    printf("%s",regular(path));
    return 0;
}
