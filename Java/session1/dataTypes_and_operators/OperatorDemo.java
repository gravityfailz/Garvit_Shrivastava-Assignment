package session1.dataTypes_and_operators;

public class OperatorDemo {

    public void arithmeticOps(int a, int b) {
        System.out.println("Arithmetic:");
        System.out.println("Sum: " + (a + b));
        System.out.println("Sub: " + (a - b));
        System.out.println("Mul: " + (a * b));
        System.out.println("Div: " + (a / b));
    }

    public void relationalOps(int a, int b) {
        System.out.println("Relational:");
        System.out.println(a > b);
        System.out.println(a < b);
        System.out.println(a == b);
    }

    public void logicalOps(boolean x, boolean y) {
        System.out.println("Logical:");
        System.out.println(x && y);
        System.out.println(x || y);
        System.out.println(!x);
    }

    public static void main(String[] args) {
        OperatorDemo demo = new OperatorDemo();

        demo.arithmeticOps(10, 5);
        demo.relationalOps(10, 5);
        demo.logicalOps(true, false);
    }
}