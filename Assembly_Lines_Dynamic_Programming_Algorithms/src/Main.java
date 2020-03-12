import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Scanner;

public class Main {

    static int lanes = 2;
    static int stations = 32;
    static int counter = 0;         // To count the steps (comparisons and array assignments)

    // Minimum function

    static int min(int a, int b)
    {
        counter++;
        return a < b ? a : b;

    }


    static int assemblyTwoLanes(int entry[], int exit[], int p[][], int t[][])
    {
        int lane1[] = new int[stations];		// Solution Arrays
        int lane2[] = new int[stations];

        int i;

        // Add first entry times + processing times to final solution arrays
        lane1[0] = entry[0] + p[0][0];
        counter++;
        lane2[0] = entry[1] + p[1][0];
        counter++;



        // Fill solution arrays with a loop
        for (i = 1; i < stations; i++)
        {
            lane1[i] = min(lane1[i - 1] + p[0][i],
                    lane2[i - 1] + t[1][i-1] + p[0][i]);
            counter++;
            lane2[i] = min(lane2[i - 1] + p[1][i],
                    lane1[i - 1] + t[0][i-1] + p[1][i]);
            counter++;
        }

        System.out.println(Arrays.toString(lane1));     // print out final arrays
        System.out.println(Arrays.toString(lane2));

        // add exit times to final arrays

        return min(lane1[stations-1] + exit[0],
                lane2[stations-1] + exit[1]);
    }

    // To print 2D arrays for troubleshooting
    public static void print2D(int mat[][])
    {
        // Loop through all rows
        for (int i = 0; i < mat.length; i++)

            // Loop through all elements of current row
            for (int j = 0; j < mat[i].length; j++)
                System.out.print(mat[i][j] + " ");
    }

    public static void main(String[] args) throws FileNotFoundException {

        File file = new File("TwoLaneTransitions.txt");

        int[][] transition_times = new int[lanes][stations - 1];


        Scanner fscan = new Scanner(file);

        int i;
        int j = 0;

        // Read in transition times array
        do {
            i = 0;
            transition_times[i][j] = fscan.nextInt();
            counter++;
            i = 1;
            transition_times[i][j] = fscan.nextInt();
            counter++;
            j++;
        } while (j < stations -1);

        fscan.close();

        //System.out.println("Transition Times Array: ");     // Print array for troubleshooting
        //print2D(t);
        //System.out.println(" ");





        File test = new File("ProcessTimes.txt");

        int[][] processing_times = new int[lanes][stations];

        Scanner fscan1 = new Scanner(test);

        int[] entry = new int[2];
        int[] exit = new int[2];

        // Read in entry and exit arrays
        entry[0] = fscan1.nextInt();
        counter++;
        entry[1] = fscan1.nextInt();
        counter++;
        fscan1.nextInt();
        exit[0] = fscan1.nextInt();
        counter++;
        exit[1] = fscan1.nextInt();
        counter++;
        fscan1.nextInt();

        // Read in processing times array
        j = 0;
        while (j < stations){
            i = 0;
            processing_times[i][j] = fscan1.nextInt();
            counter++;
            i = 1;
            processing_times[i][j] = fscan1.nextInt();
            counter++;
            fscan1.nextInt();
            j++;
        }

        //System.out.println("Process Times Array: ");          // print array for troubleshooting
        //print2D(a);

        System.out.println(" ");
        System.out.println("Entry Times: " + Arrays.toString(entry));
        System.out.println("Exit Times: " + Arrays.toString(exit));
        fscan1.close();

        long start_time = System.nanoTime();


        System.out.println(assemblyTwoLanes(entry, exit, processing_times, transition_times));

        long end_time = System.nanoTime();

        long timeElapsed = end_time - start_time;



        System.out.println("Execution time in nanoseconds: "+ timeElapsed);
        System.out.println("Execution time in milliseconds: "+ timeElapsed/1000000.0);
        System.out.println("Steps: "+ counter);


    }
}

