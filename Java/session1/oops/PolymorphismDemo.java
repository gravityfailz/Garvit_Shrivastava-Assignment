package session1.oops;

public class PolymorphismDemo {

    // Method Overloading
    public int add(int a, int b) {
        return a + b;
    }

    public double add(double a, double b) {
        return a + b;
    }

    public static void main(String[] args) {

        // Method Overloading
        PolymorphismDemo obj = new PolymorphismDemo();
        System.out.println("Sum int: " + obj.add(5, 10));
        System.out.println("Sum double: " + obj.add(5.5, 2.5));

        // Method Overriding
        Student student = new GraduateStudent("Garvit", 101, 85.5, "Computer Science");
        student.displayDetails(); // Runtime polymorphism
    }
}