package com.example.session3.controller;

import com.example.session3.model.User;
import com.example.session3.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    // ✅ Constructor Injection
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // 🔍 SEARCH API
    @GetMapping("/search")
    public ResponseEntity<List<User>> searchUsers(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) Integer age,
            @RequestParam(required = false) String role) {

        return ResponseEntity.ok(userService.searchUsers(name, age, role));
    }

    // ❌ DELETE API
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteUser(
            @PathVariable Long id,
            @RequestParam(required = false, defaultValue = "false") boolean confirm) {

        userService.deleteUser(id, confirm);
        return ResponseEntity.ok("User deleted successfully");
    }

    // ➕ SUBMIT API
    @PostMapping("/submit")
    public ResponseEntity<String> submitUser(@RequestBody User user) {

        if (user.getName() == null || user.getName().isEmpty()
                || user.getAge() == null
                || user.getRole() == null || user.getRole().isEmpty()) {

            return ResponseEntity.badRequest().body("Invalid input");
        }

        return ResponseEntity.status(201).body("User submitted successfully");
    }
}