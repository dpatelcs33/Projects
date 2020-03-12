#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <unistd.h>
#include <errno.h>

//This is an example to demonstrate how to create, initialize and access semaphores using UNIX system calls.
//Compile this program with SemSupport.c where waitS() and signalS() have been defined.
//Look at the UNIX man pages to better understand each of the semaphore functions.

extern int waitS(int);
extern int signalS(int);

#define SEM_MODE 0600  //Only owner of the process can access the semaphore.

union semun {         //This union is required as a paramter to semctl(..)
      int val;        //Used when "cmd" is SETVAL
      struct semid_ds *buf;
      ushort *array;  //Used when "cmd" is GETALL and SETALL
};

int main(){

	int mutex; 
	int s;
	int pid;
	int nop;
	union semun initial_value;
	int errno;


	//Get a semaphore
	mutex = semget(IPC_PRIVATE, 1, SEM_MODE); //Get a key to a semaphore
					//IPC_PRIVATE ensures that it is a newly
					//created key.
					//"1" - 1 member of the set.
					

	if(mutex == -1){
		printf("Error getting the semaphore\n");
		return 1;
	}	

	//Initializing the semaphore
	initial_value.val = 1;
	if(semctl(mutex,0, SETVAL, initial_value) == -1){
		printf("Error setting the value\n");
	} 

   //Accessing the semaphores - Doesn't really do anything here, as there is only 1 process.
	waitS(mutex);

	printf("c \n");

	signalS(mutex);

 
	//Removing the semaphore
   if(semctl(mutex, 0, IPC_RMID, initial_value) == -1){
        printf("Sem control error %d \n",errno);
   }

	return 1;
}
	
	

	
	
	
