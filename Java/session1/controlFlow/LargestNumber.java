package session1.controlFlow;

import java.util.Scanner;

public class LargestNumber {

    public int findLargest(int a, int b, int c) {
        int largest = a;

        if (b > largest) {
            largest = b;
        }

        if (c > largest) {
            largest = c;
        }

        return largest;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        LargestNumber obj = new LargestNumber();

        System.out.print("Enter three numbers: ");
        int a = sc.nextInt();
        int b = sc.nextInt();
        int c = sc.nextInt();

        System.out.println("Largest: " + obj.findLargest(a, b, c));

        sc.close();
    }
}