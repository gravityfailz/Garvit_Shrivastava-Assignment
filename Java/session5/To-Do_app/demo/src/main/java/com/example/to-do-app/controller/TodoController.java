package session4.To-Do_app.demo.src.main.java.com.example.to-do-app.controller;

import session4.To-Do_app.demo.src.main.java.com.example.to-do-app.dto.TodoDTO;
import session4.To-Do_app.demo.src.main.java.com.example.to-do-app.service.TodoService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
@RequestMapping("/todos")
public class TodoController {

    private static final Logger logger = LoggerFactory.getLogger(TodoController.class);

    private final TodoService service;

    public TodoController(TodoService service) {
        this.service = service;
    }

    @PostMapping
    public TodoDTO create(@RequestBody @Valid TodoDTO dto) {
        logger.info("API CALL: Create TODO");
        return service.createTodo(dto);
    }

    @GetMapping
    public List<TodoDTO> getAll() {
        logger.info("API CALL: Get all TODOs");
        return service.getAllTodos();
    }}

    private final TodoService service;

    public TodoController(TodoService service) {
        this.service = service;
    }

    @PostMapping
    public TodoDTO create(@RequestBody @Valid TodoDTO dto) {
        return service.createTodo(dto);
    }

    @GetMapping
    public List<TodoDTO> getAll() {
        return service.getAllTodos();
    }

    @GetMapping("/{id}")
    public TodoDTO getById(@PathVariable Long id) {
        return service.getTodoById(id);
    }

    @PutMapping("/{id}")
    public TodoDTO update(@PathVariable Long id, @RequestBody @Valid TodoDTO dto) {
        return service.updateTodo(id, dto);
    }

    @DeleteMapping("/{id}")
    public String delete(@PathVariable Long id) {
        service.deleteTodo(id);
        return "Deleted successfully";
    }
}