package session1.advance;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class FileReadDemo {

    public void readFile(String filePath) {
        try {
            File file = new File(filePath);
            Scanner sc = new Scanner(file);

            while (sc.hasNextLine()) {
                System.out.println(sc.nextLine());
            }

            sc.close();
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
        }
    }

    public static void main(String[] args) {
        FileReadDemo obj = new FileReadDemo();
        obj.readFile("./java/session1/advance/sample.txt");
    }
}
