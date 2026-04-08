package session1.stringsManipulation;

import java.util.Scanner;

public class ReverseString {

    public String reverse(String input) {
        String reversed = "";

        for (int i = input.length() - 1; i >= 0; i--) {
            reversed += input.charAt(i);
        }

        return reversed;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ReverseString obj = new ReverseString();

        System.out.print("Enter string: ");
        String str = sc.nextLine();

        System.out.println("Reversed: " + obj.reverse(str));

        sc.close();
    }
}
