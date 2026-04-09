package session1.advance;

abstract class Animal {
    abstract void sound();

    void sleep() {
        System.out.println("Sleeping...");
    }
}

class Dog extends Animal {
    void sound() {
        System.out.println("Dog barks");
    }
}

public class AbstractClassDemo {

    public static void main(String[] args) {
        Animal obj = new Dog();
        obj.sound();
        obj.sleep();
    }
}
