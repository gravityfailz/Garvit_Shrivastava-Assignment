package session1.dataTypes_and_operators;

import java.util.Scanner;

public class TemperatureConverter {

    public double celsiusToFahrenheit(double celsius) {
        return (celsius * 9 / 5) + 32;
    }

    public double fahrenheitToCelsius(double fahrenheit) {
        return (fahrenheit - 32) * 5 / 9;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        TemperatureConverter converter = new TemperatureConverter();

        System.out.println("1. Celsius to Fahrenheit");
        System.out.println("2. Fahrenheit to Celsius");

        int choice = sc.nextInt();

        if (choice == 1) {
            System.out.print("Enter Celsius: ");
            double c = sc.nextDouble();
            System.out.println("Fahrenheit: " + converter.celsiusToFahrenheit(c));
        } else {
            System.out.print("Enter Fahrenheit: ");
            double f = sc.nextDouble();
            System.out.println("Celsius: " + converter.fahrenheitToCelsius(f));
        }

        sc.close();
    }
}