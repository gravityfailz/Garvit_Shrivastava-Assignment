package session1.controlFlow;

import java.util.Scanner;

public class MultiplicationTable {

    public void printTable(int number) {
        for (int i = 1; i <= 10; i++) {
            System.out.println(number + " x " + i + " = " + (number * i));
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        MultiplicationTable table = new MultiplicationTable();

        System.out.print("Enter number: ");
        int num = sc.nextInt();

        table.printTable(num);

        sc.close();
    }
}
