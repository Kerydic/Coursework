#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char **argv)
{
  DIR *dirp;
  struct dirent *direntp;

   
  dirp=opendir(argv[1]);
  while((direntp=readdir(dirp))!=NULL)
  {
    if(direntp->d_name[0] == '.' || strcmp(direntp->d_name,"..") == 0){
      continue;
    }
    printf("%s\n",direntp->d_name);

  }
  closedir(dirp);
  exit(0);
  
}

