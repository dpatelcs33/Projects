#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>


//Functions to access semaphores.
//waitS() - The function equivalent to wait() in William Stallings' "Operating Systems".
//signalS() - The function equivalent to signal() in William Stallings' "Operating Systems".

void waitS(int semid){

//Initialize values

	struct sembuf op = {0, -1, 0}; //defined in sys/sem.h

	//printf("%d, %d, %d\n", op.sem_num, op.sem_op, op.sem_flg);

	if((semop(semid, &op, 1)) == -1){
		perror("Error: semop_wait");
		//printf("Semaphore wait did not succeed\nError: %d\n", errno);
		
	}

}

void signalS(int semid){

	
	struct sembuf op = {0, +1, 0};


	if(semop(semid, &op, 1) == -1){ //Semaphore operation on sempahpore with key "semid"
		perror("Error: semop_signal");
		
	
	}
}


