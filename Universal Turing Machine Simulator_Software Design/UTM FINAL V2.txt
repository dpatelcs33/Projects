
//UTM Simulator
//Created by: Kristina Mendela, Dhaval Patel, Jordan McGarty

import java.util.*;

public class UTM {

    static int currentState = 0;
    static char[] tape;
    static int head;
    static int[] transitionsUsed = new int[72 + 72 +72];
    static int transitionIndex;
    static int transUsedIndex = 0;


    //sortTransitions
    //sorts transition array by first column
    public void sortTransitions(char transitionArray[][]) {
        java.util.Arrays.sort(transitionArray, java.util.Comparator.comparing(a -> a[0]));
    }

    //getTransition method
    public static int getTransition(char transitionArray[][]) {


        for(int i = 0; i < transitionArray.length; i++ ) {

            if(currentState == Character.getNumericValue(transitionArray[i][0])) { //match the current state to the transition

                if(tape[head] == transitionArray[i][1]) { //match the input character to the transition

                    //save the index of the transition that matches
                    transitionIndex = i;


                    break;
                }
            }
        }

        //save the index in an array of the transitions we used
        transitionsUsed[transUsedIndex] = transitionIndex + 1;

        transUsedIndex = transUsedIndex + 1; //this is a counter that keeps track of where we are in the transitionsUsed array

        return transitionIndex;
    }


    //executeTransition method
    //includes pulling out values for the output, next state, and head direction
    public static void executeTransition(char[][] transitionArray) {

        //replacing char on the tape
        tape[head] = transitionArray[transitionIndex][3];

        //updating the current state to the next state
        currentState = Character.getNumericValue(transitionArray[transitionIndex][2]);

        //updates the user on which state the machine is in
        System.out.println("The Turing Machine is entering state " + currentState);

        //move the head on the tape, moving left and right
        if (transitionArray[transitionIndex][4] == 'l') {
            head = head - 1;
        }
        else if (transitionArray[transitionIndex][4] == 'r') {
            head = head + 1;
        }

    }

    //initializeArray
    //initializes the array with/without bounds
    public static void initializeArray(String w, String bound) {

        if(bound.equals("l")) { //if the variable bound = left
            char firstChar = w.charAt(0);
            if(firstChar != '>') { //if the first char is not a >
                tape = new char [72 + 72];
                tape[0] = '>';// initialize the type and write > at [0]
                head = 1;

                for(int i = 1; i < 144; i++) { //fill the initial tape with underscores
                    tape[i] = '_';
                }

                for(int i = 1; i <= w.length(); i++) { //input the input string
                    tape[i] = w.charAt(i - 1);
                }
            }
            else {
                tape = new char [72 + 72]; //initialize array with string that includes >
                head = 1;
                for(int i = 0; i < 144; i++) { //fill initial tape with underscores
                    tape[i] = '_';
                }
                for(int i = 0; i < w.length(); i++) { //input the input string
                    tape[i] = w.charAt(i);
                }
            }
        }
        else if(bound.equals("r")) { //if the bound is right bound
            char lastChar = w.charAt(w.length() - 1);
            if(lastChar != '<') { //if the last char is not a <
                tape = new char [72 + 72];
                for(int i = 0; i < 144; i++) { //fill initial tape with underscores
                    tape[i]= '_';
                }
                tape[143] = '<';// initialize the tape and write < at [144]
                int n = 1;
                for(int i = 0; i < w.length(); i++) { //input the input string

                    tape[142 - i] = w.charAt(w.length() - n);
                    n++;

                }
                head = 143 - w.length();

            }
            else {
                tape = new char [72 + 72]; //initialize array with string that includes <
                for(int i = 0; i < 144; i++) { //fill initial tape with underscores
                    tape[i]= '_';
                }

                int n = 1;
                for(int i = 0; i < w.length(); i++) { //input the input tape
                    tape[143 - i] = w.charAt(w.length() - n);
                    n++;
                }

                head = 144 - w.length();

            }

        }
        else if(bound.equals("lr")) { // linear bounded
            char firstChar = w.charAt(0);
            char lastChar = w.charAt(w.length() - 1);

            if(firstChar != '>') {
                tape = new char [w.length() + 2]; //initialize tape and input > as first in tape if not present in string
                tape[0] = '>';
                head = 1;
                if(lastChar != '<') {
                    tape[w.length() + 1] = '<'; //input < in last index if not present in the string

                    for(int i = 1; i < w.length() + 1; i++) { //loop through the string and input onto tape
                        tape[i] = w.charAt(i - 1);
                    }
                }
            }
            else {
                tape = new char [w.length()]; //initialize array with string that includes >, <
                head = 1;
                for(int i = 0; i < w.length(); i++) { //input the input string
                    tape[i] = w.charAt(i);
                }
            }


        }
        else {
            tape = new char [72 + 72 + 72]; //unbounded
            head = 72;
            for(int i = 0; i < 216; i++) {
                if(i < 72 || i >= 72 + w.length()) { //fill initial tape with underscores where there isnt a input char
                    tape[i]= '_';
                }
                else {

                    tape[i] = w.charAt(i - 72); //loop through the string and input onto tape

                }

            }
        }
    }

    public static void main(String[] args) {

        Scanner keyboard = new Scanner(System.in);

        // Transitions
        System.out.println("How many Transitions? : "); //user input number of transitions
        int count = keyboard.nextInt();
        keyboard.nextLine();
        char[][] transitionArray = new char[count][5];
        System.out.println("Enter transitions below in the format (i, Σ, j, Γ, L or R) in a list with 1 transition per line (NO SPACES; Use \'_\' for Deltas) \n\n For Example: δ(q0, a) → (q1, x, R)        0,a,1,x,R\n              δ(q1, b) → (q7, 0, R) >>>>>> 1,b,7,0,R\n              δ(q3, Δ) → (q4, Δ, L)        3,_,4,_,L"); //user input transitions

        String input;
        System.out.println(" ");
        System.out.println("Enter Transitions: ");
        for(int i = 0; i<count; i++){

            input = keyboard.nextLine();
            input = input.toLowerCase().replace(",", "");
            for (int j = 0; j<input.length(); j++){
                transitionArray[i][j] = input.charAt(j);
            }
        }


        // Input String/Tape, Final States and Bound
        System.out.println("What is the final state? (Integer): "); //user defines final state
        int final_state = keyboard.nextInt();
        keyboard.nextLine();

        System.out.println("Enter the input tape characters without spaces or commas: "); //user defines input string
        String w = keyboard.nextLine();

        System.out.println("Is the tape Left-bounded(L), Right-bounded(R), Left and Right bounded(LR) or Unbounded(U): "); //user defines bounds
        String bound = keyboard.nextLine();
        bound = bound.toLowerCase();
        initializeArray(w, bound);

        System.out.println("The Turing Machine starts at state 1");

        for(int i = 0; i < transitionsUsed.length; i++ ) { //fill transitionsUsed array with underscores
            transitionsUsed[i] = '_';
        }


        // START
        while(true){
            try {           // Catch Index out of bounds Exceptions and handle them

                getTransition(transitionArray);		// Try and read the position at "head" to get transition


            }catch (ArrayIndexOutOfBoundsException e) {		// If exception occurs then

                System.out.println("Index out of bounds Exception: Handling and retrying!");

                if (bound.equals("l")) {    // If Left-bounded, Extend right side
                    tape = Arrays.copyOf(tape, head+100);	// Copy old array and extend it 100

                    for (int i = head; i < head+100; i++) {	// Fill with underscore
                        tape[i] = '_';

                    }
                }

                else if (bound.equals("r")) {   // If right-bounded, Extend left side

                    int tape_size = tape.length;	//Save old array size


                    tape = Arrays.copyOf(tape,  tape.length + 150);	// Copy old array and extend it 150
                    int current = tape.length;
                    for(int i = tape_size; i > tape_size; i--) {	// Move old array over all the way right
                        char temp = tape[i];
                        tape[i] = '_';
                        tape[current] = temp;
                        current--;
                    }

                    head = head+150;		// Move the head
                }

                else if (bound.equals("u")){

                    if (head == -1) {		// If space runs out on the left

                        int tape_size = tape.length;

                        tape = Arrays.copyOf(tape,  tape.length + 150);	// Copy old array and extend it
                        int current = tape.length;
                        for(int i = tape_size; i > tape_size; i--) {	// Move old array over all the way right
                            char temp = tape[i];
                            tape[i] = '_';
                            tape[current] = temp;
                            current--;
                        }

                        head = head+150;	// Move head to appropriate spot
                    }

                    else {	// Otherwise it ran out of space on the right

                        tape = Arrays.copyOf(tape, head+100);	// Copy old array and extend it 100

                        for (int i = head; i < head+100; i++) {	// Fill with underscores
                            tape[i] = '_';

                        }

                    }
                }

                getTransition(transitionArray);
            }

            //getTransition(transitionArray);
            executeTransition(transitionArray);
            if (currentState == final_state){
                break;
            }
        }
        //output formatting
        System.out.println("HALT");
        System.out.println("\n");
        System.out.print("Output Tape: [");
        for(int i = tape.length - 1; i > 0 ; i--) {

            if(tape[i] != '_') {
                System.out.print(tape[i] + ",");
            }

        }
        System.out.print("\b");
        System.out.print("]");
        System.out.println("\n");

        System.out.print("The transitions used were: [");
        for(int i = 0; i < transitionsUsed.length; i++){

            if(transitionsUsed[i] != '_')
                System.out.print(transitionsUsed[i] + ",");

        }
        System.out.print("\b");
        System.out.print("]");
    }


}






