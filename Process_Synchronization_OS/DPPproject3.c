#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <errno.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/wait.h>


//Semaphore
extern int waitS(int);
extern int signalS(int);

#define SEM_MODE 0600 //Only owner of the process can access the semaphore.


union semun {         //This union is required as a paramter to semctl(..)
      int val;        //Used when "cmd" is SETVAL
      struct semid_ds *buf;
      ushort *array;  //Used when "cmd" is GETALL and SETALL
};



void work(int pIndex){
	
	//work specific declarations
	//int *array = NULL;
	FILE *infile;
	FILE *outfile;
	int count = 0;
	int temp;

	infile = fopen("common.txt", "r");

	if ( infile == NULL ) {  // error checking with fopen call
    printf("Unable to open file. Make sure to put the \'common.txt\' file in the working directory."); 
    exit(1);
  	} 


  	//Count numbers in file
	while(fscanf(infile, "%d", &temp) == 1){
		count++;
	}
    
	fclose(infile);	//Close file and reopen to reset fscanf

	int file_array[count]; // Initialize array to the size of counted numbers
	
	infile = fopen("common.txt", "r");
	for (int i = 0; i < count; i++){
		fscanf(infile, "%d", &file_array[i]);
	}

	int size = count;	// set size variable to count for easier tracking

	// Print Original Array	
	printf("\nArray Before Work: [");	
	for (int i = 0 ; i < size; i++){
		
		printf("%d ", file_array[i]);
	}
	printf("]\n");

	//Start operations on array
	temp = file_array[0] - 1;

	if (temp < size){
	 	file_array[temp] = pIndex;
	 	file_array[0] = file_array[0] + 1;
	}

	else{
		printf("IndexOutOfBounds: Cycling back to beginning of array (Skipping over first number)\n");
	 	file_array[(temp % size) + 1] = pIndex;
	 	file_array[0] = file_array[0] + 1;
	}

	//Print array after work
	printf("Array after work: [");	
	for (int i = 0 ; i < size; i++){
		
		printf("%d ", file_array[i]);
	}
	printf("]\n\n");


	//Write array back to file and close file
	outfile = fopen("common.txt", "w");
	for (int i = 0; i < size; i++){
		fprintf(outfile, "%d ", file_array[i]);
	}
	fclose(outfile);

}


	
int main() {

	// Data declarations
	int numOfChildren, numOfRuns, pIndex;
	pid_t *childrenPid;
	int mutex;
	int pid;
	union semun initial_value;
	// For wait system call
	int status = 0;
	int wpid;
	int child_pid;


	//Get a semaphore
	mutex = semget(IPC_PRIVATE, 1, SEM_MODE);

	//Check status of semaphore
	if(mutex == -1){
		printf("Error getting the semaphore\n");
		return 1;
	}


	//Initializing the semaphore and checking status again
	initial_value.val = 1;

	if (semctl(mutex, 0, SETVAL, initial_value) == -1){
		printf("Error setting the value\n");
	}
	

	// Step 1: Prompt user for # of children.
	printf("Enter number of Children: ");
	scanf("%d", &numOfChildren);
		
	// Step 2: Prompt user for # of runs.
	printf("Enter number of Runs: ");
	scanf("%d", &numOfRuns);
	

	// Step 3 - Execute
	printf("\nThis is the Parent; my pID is %d \n\n", getpid());
			
	for (int i = 1; i <= numOfChildren; i++) {

		waitS(mutex); // start critical section
		
		if ((child_pid = fork()) == 0) {
			pIndex = i;
			int pid = getpid();
			int ppid = getppid();
			
					
			printf("\n****This is Child %d; my pID is %d; my parent's pID is %d**** \n\n", pIndex, pid, ppid);
				

			for (int j = 1; j <= numOfRuns; j++) {

				printf("-----------Child %d - RUN # %d-----------\t\n", pIndex, j);

				work(pIndex); // Do work
				
			}
			signalS(mutex);
			exit(0);
		}
		
				
		else if (child_pid < 0) {
				printf("Error forking! Try Again! \n");
				return 1;
		}

	}

	while ((wpid = wait(&status)) > 0);  // wait for wait() to error out when no chld processes remain

	//Remove Semaphore and handle error
	if(semctl(mutex, 0, IPC_RMID, initial_value) == -1){
 		
 		perror("Error removing sem (semctl)");
    }

	return 0;
}
