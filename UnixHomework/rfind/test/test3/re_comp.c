#include <stdio.h>
#include <sys/types.h>
#include <string.h>
#include <regex.h>
#include <fcntl.h>
#include <unistd.h>

int comp(char *path,char *buffer){
	int status, i;
	int cflags = REG_EXTENDED;
	regmatch_t pmatch[1];
	const size_t nmatch = 1;
	regex_t reg;
	const char * pattern = buffer;

	regcomp(&reg, pattern, cflags);

	int file = open(path,O_RDONLY);

	char buffer_0[2048];
	int read_n;
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

int main(int argc,char *argv[]){
	char *path = "test.c";
	char *buffer = ".*gee.*().*";
	if(comp(path,buffer)==1){
		printf("match failed!");
	}else if(comp(path,buffer)==0){
		printf("match success!");
	}
	return 0;
	
}