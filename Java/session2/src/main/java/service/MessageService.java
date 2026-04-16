package session2.src.main.java.service;

import component.MessageFormatter;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class MessageService {

    private final Map<String, MessageFormatter> formatterMap;

    public MessageService(Map<String, MessageFormatter> formatterMap) {
        this.formatterMap = formatterMap;
    }

    public String getMessage(String type) {

        MessageFormatter formatter = formatterMap.get(type.toLowerCase() + "Formatter");

        if (formatter == null) {
            return "Invalid message type";
        }

        return formatter.format();
    }
}