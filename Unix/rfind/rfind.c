#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <regex.h>
#include <fcntl.h>
#include <unistd.h>

// Splicing two strings and return a pointer
char* join(char *s1, char *s2)
{
    char *result = malloc(strlen(s1)+strlen(s2)+1);
    if (result == NULL) exit (1);

    strcpy(result, s1);
    strcat(result, s2);

    return result;
}

// Preprocessor of regular expression
char *regular(char *path_0){
	char *path = malloc(16);
	char *path_1 = malloc(16);
	strcpy(path,path_0);
    for(int i = 0;i < sizeof(path);i++){
        if(path[i]=='*'){
            for(int j = sizeof(path);j >= i;j--){
                path[j+1] = path[j];
            }
            path[i] = '.';
            i++;
        }
        if(path[i]=='.'){
        	for(int j = sizeof(path);j >= i;j--){
                path[j+1] = path[j];
            }
            path[i] = '\\';
            i++;
        }
    }
    strcpy(path_1,path);
    return path_1;
}

// Compare path(the file name) to file_name(the input)
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
    return 0;
}

// Compare path(the file content) to buffer(the processed inputed regular expression)
int judge_bycontent(char *path, char *buffer){
    int status;
    int cflags = REG_EXTENDED;
    regmatch_t pmatch[1];
    const size_t nmatch = 1;
    regex_t reg;
    const char * pattern = regular(buffer);

    regcomp(&reg, pattern, cflags);

    int file = open(path,O_RDONLY);

    char buffer_0[2048];
    ssize_t read_n;
    read_n = read(file,buffer_0,2048);
    char *buf = buffer_0;
    if(read_n!=-1){
        status = regexec(&reg, buf, nmatch, pmatch, 0);
        if(status == REG_NOMATCH){
            return 1;
            // not match
        }else if(status == 0){
            // match
            return 0;
        }

    }
    regfree(&reg);
    return 0;
}

// Search file by name and content judged by oper in path
int find_n(int oper,char *path,char *name_content,char *name_content_1){
    DIR *dirp;
    struct dirent *direntp;
    dirp=opendir(path);

    if(!dirp){
        return 1;
    }

    while((direntp=readdir(dirp))!=NULL)
    {
        if(direntp->d_name[0] == '.' || strcmp(direntp->d_name,"..") == 0){
            continue;
        }
        if(direntp->d_type == 4){
            char *path_1;
            if(strcmp(path,"/")==0){
                path_1 = join("/",direntp->d_name);
            }else{
                path_1 = join(join(path,"/"),direntp->d_name);
            }
            find_n(oper,path_1,name_content,name_content_1);
        }
        if(direntp->d_type == 8){
            if(oper == 1&&judge_byname(direntp->d_name,name_content)==0){
                printf("file founded! location:%s\n",join(join(path,"/"),direntp->d_name));
            }else if(oper == 2&&judge_bycontent(join(join(path,"/"),direntp->d_name),name_content)==0){
                printf("file founded! location:%s\n",join(join(path,"/"),direntp->d_name));
            }else if(oper == 3&&judge_byname(direntp->d_name,name_content)==0
            	&&judge_bycontent(join(join(path,"/"),direntp->d_name),name_content_1)==0){
            	printf("file founded! location:%s\n",join(join(path,"/"),direntp->d_name));
            }
        }
    }
    closedir(dirp);
    return 0;
}

// First fuction to be used
void find(char *oper,char *path,char *name_content,char *name_content_1){
    if(strcmp(oper,"-name")==0){
        find_n(1,path,name_content,NULL);
    }else if(strcmp(oper,"-content")==0){
        find_n(2,path,name_content,NULL);
    }else if(strcmp(oper,"-name-content")==0){
        find_n(3,path,name_content,name_content_1);
    }
}

int main (int argc, char *argv[]){
	if(argc == 4){
		find(argv[1],argv[3],argv[2],NULL);
		return 0;
	}else if(argc == 6){
		if(strcmp(argv[1],"-name")==0 && strcmp(argv[3],"-content")==0){
			find("-name-content",argv[5],argv[2],argv[4]);
		}else if(strcmp(argv[3],"-name")==0 && strcmp(argv[1],"-content")==0){
			find("-name-content",argv[5],argv[4],argv[2]);
		}else {
			printf("Wrong operation!\nUsage:rfind -name/-content str -content/-name str dir\n");
		}
		return 0;
	}else{
		printf("Wrong operation!\nUsage:rfind -name/-content str -content/-name str dir\n");
		return 1;
	}
}
