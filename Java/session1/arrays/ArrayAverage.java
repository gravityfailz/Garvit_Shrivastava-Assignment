package session1.arrays;

import java.util.Scanner;

public class ArrayAverage {

    public double calculateAverage(int[] arr) {
        int sum = 0;

        for (int num : arr) {
            sum += num;
        }

        return (double) sum / arr.length;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayAverage obj = new ArrayAverage();

        System.out.print("Enter number of elements: ");
        int n = sc.nextInt();

        int[] arr = new int[n];

        System.out.println("Enter elements:");
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        System.out.println("Average: " + obj.calculateAverage(arr));

        sc.close();
    }
}