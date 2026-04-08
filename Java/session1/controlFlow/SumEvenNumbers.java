package session1.controlFlow;

public class SumEvenNumbers {

    public int calculateSum() {
        int sum = 0;
        int i = 1;

        while (i <= 10) {
            if (i % 2 == 0) {
                sum += i;
            }
            i++;
        }

        return sum;
    }

    public static void main(String[] args) {
        SumEvenNumbers obj = new SumEvenNumbers();
        System.out.println("Sum of even numbers (1-10): " + obj.calculateSum());
    }
}
