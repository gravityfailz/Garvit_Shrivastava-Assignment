package session1.advance;

public class ExceptionHandlingDemo {

    public void divide(int a, int b) {
        try {
            int result = a / b;
            System.out.println("Result: " + result);
        } catch (ArithmeticException e) {
            System.out.println("Error: Cannot divide by zero");
        } finally {
            System.out.println("Execution completed");
        }
    }

    public static void main(String[] args) {
        ExceptionHandlingDemo obj = new ExceptionHandlingDemo();
        obj.divide(10, 0);
    }
}
