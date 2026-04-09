package session1.oops;

public class EncapsulationDemo {

    private double balance;

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }

    public void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
        }
    }

    public static void main(String[] args) {
        EncapsulationDemo account = new EncapsulationDemo();

        account.deposit(1000);
        account.withdraw(300);

        System.out.println("Balance: " + account.getBalance());
    }
}
