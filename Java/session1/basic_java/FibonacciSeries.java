package session1.basic_java;

import java.util.Scanner;

public class FibonacciSeries {

    public void printFibonacci(int limit) {
        int a = 0, b = 1;

        System.out.print("Fibonacci: " + a + " " + b + " ");

        for (int i = 2; i < limit; i++) {
            int next = a + b;
            System.out.print(next + " ");
            a = b;
            b = next;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        FibonacciSeries fib = new FibonacciSeries();

        System.out.print("Enter limit: ");
        int n = sc.nextInt();

        fib.printFibonacci(n);

        sc.close();
    }
}
