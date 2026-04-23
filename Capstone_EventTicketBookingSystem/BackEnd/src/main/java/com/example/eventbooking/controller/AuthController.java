package com.example.eventbooking.controller;

import com.example.eventbooking.dto.UserRequestDTO;
import com.example.eventbooking.dto.UserResponseDTO;
import com.example.eventbooking.service.UserService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserService userService;

    public AuthController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/register")
    public UserResponseDTO register(@Valid @RequestBody UserRequestDTO request) {
        return userService.register(request);
    }

    @PostMapping("/login")
    public UserResponseDTO login(@RequestParam String email,
            @RequestParam String password) {
        return userService.login(email, password);
    }
}