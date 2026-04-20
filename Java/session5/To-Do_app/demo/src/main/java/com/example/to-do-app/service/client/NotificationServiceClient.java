package session5.To-Do_app.demo.src.main.java.com.example.to-do-app.service.client;

import org.springframework.stereotype.Component;

@Component
public class NotificationServiceClient {

    public void sendNotification(String message) {
        System.out.println("Notification sent: " + message);
    }
}
