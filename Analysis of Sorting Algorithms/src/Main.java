import jsjf.LinkedList;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Scanner;
import sort.InsertionSortLinkedList;

//import java.util.concurrent.TimeUnit;

public class Main {

    public static void main(String[] args) throws FileNotFoundException {
        File file = new File("inorder10k.txt");

        LinkedList list = new LinkedList();

        Scanner sc = new Scanner(new FileInputStream(file));

        while (sc.hasNextInt()){
            list.add(sc.nextInt());
        }

        sc.close();

        long start_time = System.nanoTime();

        //System.out.println(list.toString());

        LinkedList sorted = InsertionSortLinkedList.insertionSort(list);

        long end_time = System.nanoTime();

        long timeElasped = end_time - start_time;

        //System.out.println(sorted.toString());


        System.out.println("Execution time in nanoseconds: "+ timeElasped);
        System.out.println("Execution time in milliseconds: "+ timeElasped/1000000.0);
        System.out.println("Steps: "+ InsertionSortLinkedList.steps);
    }
}
