package session4.To-Do_app.demo.src.main.java.com.example.to-do-app.service;

import session4.To-Do_app.demo.src.main.java.com.example.to-do-app.dto.TodoDTO;
import session4.To-Do_app.demo.src.main.java.com.example.to-do-app.Todo.Status;
import session4.To-Do_app.demo.src.main.java.com.example.to-do-app.exception.ResourceNotFoundException;
import session4.To-Do_app.demo.src.main.java.com.example.to-do-app.repository.TodoRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class TodoService {

    private final TodoRepository repository;

    public TodoService(TodoRepository repository) {
        this.repository = repository;
    }

    // CREATE
    public TodoDTO createTodo(TodoDTO dto) {

        Todo todo = TodoMapper.toEntity(dto);

        if (dto.getStatus() == null) {
            todo.setStatus(Status.PENDING);
        } else {
            todo.setStatus(Status.valueOf(dto.getStatus()));
        }

        todo.setCreatedAt(LocalDateTime.now());

        return TodoMapper.toDTO(repository.save(todo));
    }

    // GET ALL
    public List<TodoDTO> getAllTodos() {
        return repository.findAll()
                .stream()
                .map(TodoMapper::toDTO)
                .toList();
    }

    // GET BY ID
    public TodoDTO getTodoById(Long id) {
        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id " + id));

        return TodoMapper.toDTO(todo);
    }

    // UPDATE
    public TodoDTO updateTodo(Long id, TodoDTO dto) {
        Todo todo = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Todo not found with id " + id));

        // Status transition rule
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

    // DELETE
    public void deleteTodo(Long id) {
        if (!repository.existsById(id)) {
            throw new ResourceNotFoundException("Todo not found with id " + id);
        }
        repository.deleteById(id);
    }
}