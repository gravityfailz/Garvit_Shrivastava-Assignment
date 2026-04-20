package session4.To-Do_app.demo.src.main.java.com.example.to-do-app.service;

import com.example.demo.dto.TodoDTO;
import com.example.demo.entity.Todo;

public class TodoMapper {

    public static TodoDTO toDTO(Todo todo) {
        TodoDTO dto = new TodoDTO();

        dto.setId(todo.getId());
        dto.setTitle(todo.getTitle());
        dto.setDescription(todo.getDescription());
        dto.setStatus(todo.getStatus().name());
        dto.setCreatedAt(todo.getCreatedAt());

        return dto;
    }

    public static Todo toEntity(TodoDTO dto) {
        Todo todo = new Todo();

        todo.setTitle(dto.getTitle());
        todo.setDescription(dto.getDescription());

        return todo;
    }
}
