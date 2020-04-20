#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <string.h>


int main(int argc, char *argv[]){
	if(argc != 3){
		printf("Please input right location!\n");
		return 1;
	}

	int fileIn = open(argv[1],O_RDONLY);
	if(fileIn==-1){
		printf("Failed to open the input file!\n");
		return 1;
	}

	int fileOut = open(argv[2],O_WRONLY|O_CREAT,S_IRWXU | S_IRWXG | S_IRWXO);
	if(fileOut==-1){
		struct stat st;
 		stat(argv[2],&st);
		if(S_ISDIR(st.st_mode)){
			fileOut = open(strcat(strcat(argv[2],"/"),argv[1]),O_WRONLY|O_CREAT,
				S_IRWXU | S_IRWXG | S_IRWXO);
		}else{
			printf("Failed to open the output location/file!\n");
		}
		
	}
    
	char buffer[1024];
	int read_n;
	while(true){
		read_n = read(fileIn,buffer,1024);
		if(read_n==0){
			printf("Copy succes!\n");
			return 0;
		}else if(read_n == -1){
			printf("Failed to read the file!\n");
			return 1;
		}else{
			int write_n = write(fileOut,buffer,read_n);
			if(write_n != read_n){
				printf("Failed to write the file!\n");
				return 1;
			}
		}
	}
	return 0;
}
