package session1.basic_java;

public class PatternPrinter {

    public void printTriangle(int rows) {
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        PatternPrinter printer = new PatternPrinter();
        printer.printTriangle(5);
    }
}
