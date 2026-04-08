package session1.basic_java;

import java.util.Scanner;

public class EvenOddChecker {

    public boolean isEven(int number) {
        return number % 2 == 0;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        EvenOddChecker checker = new EvenOddChecker();

        System.out.print("Enter number: ");
        int num = sc.nextInt();

        if (checker.isEven(num)) {
            System.out.println("Even");
        } else {
            System.out.println("Odd");
        }

        sc.close();
    }
}