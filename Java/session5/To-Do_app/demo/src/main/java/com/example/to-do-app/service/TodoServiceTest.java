package session5.To-Do_app.demo.src.main.java.com.example.to-do-app.service;

package com.example.demo.service;

import session5.To-Do_app.demo.src.main.java.com.example.to-do-app.dto.TodoDTO;
import session5.To-Do_app.demo.src.main.java.com.example.to-do-app.entity.Todo;
import session5.To-Do_app.demo.src.main.java.com.example.to-do-app.repository.TodoRepository;
import session5.To-Do_app.demo.src.main.java.com.example.to-do-app.service.client.NotificationServiceClient;

import org.junit.jupiter.api.Test;

import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

public class TodoServiceTest {

    @Test
    void testCreateTodo() {

        TodoRepository repo = mock(TodoRepository.class);
        NotificationServiceClient client = mock(NotificationServiceClient.class);

        TodoService service = new TodoService(repo, client);

        TodoDTO dto = new TodoDTO();
        dto.setTitle("Test Task");

        when(repo.save(any(Todo.class))).thenAnswer(i -> i.getArguments()[0]);

        TodoDTO result = service.createTodo(dto);

        assertEquals("Test Task", result.getTitle());
        verify(client, times(1)).sendNotification(anyString());
    }
}