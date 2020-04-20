#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <string.h>
#include <assert.h>

int main(int argc, char *argv[]){
	if(argc != 3){
		printf("Please input right Location!\n");
		return 1;
	}

	int fileIn = open(argv[1],O_RDONLY);
	if(fileIn==-1){
		printf("Failed to open the input file!\n");
		return 1;
	}	

	char *file2 = argv[2];
	int fileOut = open(argv[2],O_RDWR | O_CREAT | O_TRUNC, S_IRWXU | S_IRWXG | S_IRWXO);
	if(fileOut==-1){
		struct stat st;
 		stat(argv[2],&st);
		if(S_ISDIR(st.st_mode)){
			file2=strcat(strcat(argv[2],"/"),argv[1]);
			fileOut = open(file2,O_RDWR|O_CREAT|O_TRUNC,
				S_IRWXU | S_IRWXG | S_IRWXO);
		}else{
			printf("Failed to open the output location/file!\n");
			return 1;
		}	
	}

	void *start;
	void *end;
	struct stat stat1;
	fstat(fileIn, &stat1);
	truncate(file2, stat1.st_size);

	start = mmap(NULL, stat1.st_size, PROT_READ, MAP_PRIVATE, fileIn, 0);
	end = mmap(NULL, stat1.st_size, PROT_WRITE | PROT_READ, MAP_SHARED, fileOut, 0);

	if(start == MAP_FAILED){
		printf("Error!\n");		
		return 1;
	}else{
		memcpy(end,start,stat1.st_size);
		printf("Copy Success!\n");	
	}

	munmap(start, stat1.st_size);
	munmap(end, stat1.st_size);
    	close(fileIn);
	close(fileOut);

	return 0;
}
