package session1.basic_java;

import java.util.Scanner;

public class FactorialCalculator {

    public long calculateFactorial(int number) {
        long result = 1;

        for (int i = 1; i <= number; i++) {
            result *= i;
        }

        return result;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        FactorialCalculator calculator = new FactorialCalculator();

        System.out.print("Enter number: ");
        int num = sc.nextInt();

        System.out.println("Factorial: " + calculator.calculateFactorial(num));

        sc.close();
    }
}