package session5.To-Do_app.demo.src.main.java.com.example.to-do-app.service;

import session5.To-Do_app.demo.src.main.java.com.example.to-do-app.dto.TodoDTO;
import session5.To-Do_app.demo.src.main.java.com.example.to-do-app.Todo.Status;
import session5.To-Do_app.demo.src.main.java.com.example.to-do-app.exception.ResourceNotFoundException;
import session5.To-Do_app.demo.src.main.java.com.example.to-do-app.repository.TodoRepository;
import org.springframework.stereotype.Service;

import session4.To-Do_app.demo.src.main.java.com.example.to-do-app.Todo;

import session4.To-Do_app.demo.src.main.java.com.example.to-do-app.service.client.NotificationServiceClient;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class TodoService {

    private static final Logger logger = LoggerFactory.getLogger(TodoService.class);

    private final TodoRepository repository;
    private final NotificationServiceClient notificationClient;

    public TodoService(TodoRepository repository,
            NotificationServiceClient notificationClient) {
        this.repository = repository;
        this.notificationClient = notificationClient;
    }

    // CREATE
    public TodoDTO createTodo(TodoDTO dto) {

        logger.info("Creating TODO in service layer");

        Todo todo = TodoMapper.toEntity(dto);

        if (dto.getStatus() == null) {
            todo.setStatus(Status.PENDING);
        } else {
            todo.setStatus(Status.valueOf(dto.getStatus()));
        }

        todo.setCreatedAt(LocalDateTime.now());

        Todo saved = repository.save(todo);

        logger.info("Sending notification for TODO: {}", saved.getTitle());
        notificationClient.sendNotification("New TODO created: " + saved.getTitle());

        return TodoMapper.toDTO(saved);
    }

    public List<TodoDTO> getAllTodos() {
        logger.info("Fetching all TODOs");
        return repository.findAll().stream().map(TodoMapper::toDTO).toList();
    }

    public TodoDTO getTodoById(Long id) {
        logger.info("Fetching TODO by id: {}", id);

        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id " + id));

        return TodoMapper.toDTO(todo);
    }

    public TodoDTO updateTodo(Long id, TodoDTO dto) {
        logger.info("Updating TODO with id: {}", id);

        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id " + id));

        if (dto.getStatus() != null) {
            Status newStatus = Status.valueOf(dto.getStatus());

            if ((todo.getStatus() == Status.PENDING && newStatus == Status.COMPLETED) ||
                    (todo.getStatus() == Status.COMPLETED && newStatus == Status.PENDING)) {

                todo.setStatus(newStatus);
            } else {
                throw new RuntimeException("Invalid status transition");
            }
        }

        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        return TodoMapper.toDTO(repository.save(todo));
    }

    public void deleteTodo(Long id) {
        logger.info("Deleting TODO with id: {}", id);

        if (!repository.existsById(id)) {
            throw new ResourceNotFoundException("Todo not found with id " + id);
        }

        repository.deleteById(id);
    }
}