package session1.controlFlow;

import java.util.Scanner;

public class PrimeChecker {

    public boolean isPrime(int number) {
        if (number <= 1)
            return false;

        for (int i = 2; i <= number / 2; i++) {
            if (number % i == 0) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        PrimeChecker checker = new PrimeChecker();

        System.out.print("Enter number: ");
        int num = sc.nextInt();

        if (checker.isPrime(num)) {
            System.out.println("Prime Number");
        } else {
            System.out.println("Not Prime");
        }

        sc.close();
    }
}
