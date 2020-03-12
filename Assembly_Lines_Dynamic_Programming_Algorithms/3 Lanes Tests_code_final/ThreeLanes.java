import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Scanner;

public class ThreeLanes {

    static int lanes = 3;
    static int stations = 80; //declare number of lanes and number of stations
    static int counter = 0; // steps counter variable (Comparisons and Array Assignments)

    public static void main(String[] args) throws FileNotFoundException {

        File file = new File("ThreeLaneTransitions.txt");

        int[][][] t = new int[lanes][lanes][stations]; //an array of transitions, the array is set up as 3x3 grids and 1 grid for each station

        Scanner fscan = new Scanner(file);

        // Read in t
        for(int i = 0; i < stations - 1; i++) { //read in the transitions from the file
            t[0][0][i] = fscan.nextInt();
            counter++;
            t[0][1][i] = fscan.nextInt();
            counter++;
            t[0][2][i] = fscan.nextInt();
            counter++;
            t[1][0][i] = fscan.nextInt();
            counter++;
            t[1][1][i] = fscan.nextInt();
            counter++;
            t[1][2][i] = fscan.nextInt();
            counter++;
            t[2][0][i] = fscan.nextInt();
            counter++;
            t[2][1][i] = fscan.nextInt();
            counter++;
            t[2][2][i] = fscan.nextInt();
            counter++;
        }

        fscan.close();

        File test = new File("ProcessTimes.txt");

        int[][] a = new int[lanes][stations]; //array of process times from station to station

        Scanner fscan1 = new Scanner(test);

        int[] e = new int[lanes];//entry time array
        int[] x = new int[lanes];//exit time array

        // Read in e and x
        e[0] = fscan1.nextInt();
        counter++;
        e[1] = fscan1.nextInt();
        counter++;
        e[2] = fscan1.nextInt();//first line of file is entry times, give this it's own array
        counter++;

        x[0] = fscan1.nextInt();
        counter++;
        x[1] = fscan1.nextInt();
        counter++;
        x[2] = fscan1.nextInt();//second line of file is exit times, give this it's own array
        counter++;


        for(int i = 0; i < stations; i++) {
            a[0][i] = fscan1.nextInt();
            counter++;
            a[1][i] = fscan1.nextInt();
            counter++;
            a[2][i] = fscan1.nextInt();
            counter++;
            System.out.println(a[0][i] + "    "  + a[1][i] + "    " + a[2][i]);
        }

        System.out.println(Arrays.toString(e));
        System.out.println(Arrays.toString(x));
        fscan1.close();

        long start_time = System.nanoTime();


        System.out.println(minPath(a, t, e, x));

        long end_time = System.nanoTime();

        long timeElapsed = end_time - start_time;

        System.out.println("Execution time in nanoseconds: "+ timeElapsed);
        System.out.println("Execution time in milliseconds: "+ timeElapsed/1000000.0);
        System.out.println("Steps: "+ counter);


    }

    // Minimum Function
    static int min(int a, int b) {
        counter++;
        return a < b ? a : b;

    }

    static int minPath(int[][] a, int[][][] t, int e[], int x[]) {
        int Lane1[] = new int[stations + 1];
        int Lane2[] = new int[stations + 1];
        int Lane3[] = new int[stations + 1]; //create an array for each lane of the number of stations
        int i;

        // Add entry times to final solution arrays
        Lane1[0] = e[0];
        counter++;

        Lane2[0] = e[1];
        counter++;

        Lane3[0] = e[2];
        counter++;

        // Fill arrays Lane1[] and Lane2[] and Lane3[]
        for (i = 1; i < stations; i++) {
            Lane1[i] = min(Lane1[i - 1] + a[0][i],
                    min(Lane2[i - 1] + a[1][i] + t[1][0][i - 1],
                            Lane3[i - 1] + a[2][i] + t[2][0][i - 1]));
            counter++;

            Lane2[i] = min(Lane2[i - 1] + a[1][i],
                    min(Lane1[i - 1] + a[0][i] + t[0][1][i - 1],
                            Lane3[i - 1] + a[2][i] + t[2][1][i - 1]));
            counter++;

            Lane3[i] = min(Lane3[i - 1] + a[2][i],
                    min(Lane1[i - 1] + a[0][i] + t[0][2][i - 1],
                            Lane2[i - 1] + a[1][i] + t[1][2][i - 1]));
            counter++;

        }
        System.out.println();
        Lane1[stations] = Lane1[stations - 1] + a[0][stations - 1];
        counter++;
        Lane2[stations] = Lane2[stations - 1] + a[1][stations - 1];
        counter++;
        Lane3[stations] = Lane3[stations - 1] + a[2][stations - 1];
        counter++;

        System.out.println(Arrays.toString(Lane1));
        System.out.println(Arrays.toString(Lane2));
        System.out.println(Arrays.toString(Lane3));

        return min(min(Lane1[stations] + x[0], Lane2[stations] + x[1]), Lane3[stations] + x[2]); //after filling in the table, find min between the three lanes
    }

    // To print 2D arrays
    public static void print2D(int mat[][]) {
        // Loop through all rows
        for (int i = 0; i < mat.length; i++)
            // Loop through all elements of current row
            for (int j = 0; j < mat[i].length; j++)
                System.out.print(mat[i][j] + " ");
    }


}
