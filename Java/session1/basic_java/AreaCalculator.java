package session1.basic_java;

import java.util.*;

public class AreaCalculator {

    private static final double PI = 3.14159;

    public double calculateCircleArea(double radius) {
        return PI * radius * radius;
    }

    public double calculateRectangleArea(double length, double width) {
        return length * width;
    }

    public double calculateTriangleArea(double base, double height) {
        return 0.5 * base * height;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        AreaCalculator calculator = new AreaCalculator();

        System.out.println("Choose shape: 1.Circle 2.Rectangle 3.Triangle");
        int choice = sc.nextInt();

        switch (choice) {
            case 1:
                System.out.print("Enter radius: ");
                double r = sc.nextDouble();
                System.out.println("Area: " + calculator.calculateCircleArea(r));
                break;

            case 2:
                System.out.print("Enter length and width: ");
                double l = sc.nextDouble();
                double w = sc.nextDouble();
                System.out.println("Area: " + calculator.calculateRectangleArea(l, w));
                break;

            case 3:
                System.out.print("Enter base and height: ");
                double b = sc.nextDouble();
                double h = sc.nextDouble();
                System.out.println("Area: " + calculator.calculateTriangleArea(b, h));
                break;

            default:
                System.out.println("Invalid choice");
        }

        sc.close();
    }
}