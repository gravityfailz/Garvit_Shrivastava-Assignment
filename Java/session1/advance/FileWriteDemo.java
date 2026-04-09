package session1.advance;

import java.io.FileWriter;
import java.io.IOException;

public class FileWriteDemo {

    public void writeFile(String filePath) {
        try {
            FileWriter writer = new FileWriter(filePath);
            writer.write("Hello from Java File Handling!");
            writer.close();

            System.out.println("File written successfully");
        } catch (IOException e) {
            System.out.println("Error writing file");
        }
    }

    public static void main(String[] args) {
        FileWriteDemo obj = new FileWriteDemo();
        obj.writeFile("./java/session1/advance/sample.txt");
    }
}