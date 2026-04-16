package session2.src.main.java.controller;

import org.springframework.web.bind.annotation.*;
import service.MessageService;

@RestController
@RequestMapping("/message")
public class MessageController {

    private final MessageService messageService;

    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

    @GetMapping
    public String getMessage(@RequestParam String type) {
        return messageService.getMessage(type);
    }
}