package session4.To-Do_app.demo.src.main.java.com.example.to-do-app.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}