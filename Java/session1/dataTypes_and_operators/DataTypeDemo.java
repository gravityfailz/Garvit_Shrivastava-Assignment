package session1.dataTypes_and_operators;

public class DataTypeDemo {

    public void showPrimitive() {
        int number = 10;
        double price = 99.99;
        char grade = 'A';
        boolean isValid = true;

        System.out.println("Primitive Data Types:");
        System.out.println(number + ", " + price + ", " + grade + ", " + isValid);
    }

    public void showReference() {
        String name = "Garvit";
        int[] arr = { 1, 2, 3 };

        System.out.println("Reference Data Types:");
        System.out.println("Name: " + name);
        System.out.println("Array first element: " + arr[0]);
    }

    public static void main(String[] args) {
        DataTypeDemo demo = new DataTypeDemo();
        demo.showPrimitive();
        demo.showReference();
    }
}