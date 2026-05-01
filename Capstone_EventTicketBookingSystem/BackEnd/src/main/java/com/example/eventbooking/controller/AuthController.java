package com.example.eventbooking.controller;

import com.example.eventbooking.config.JwtUtil;
import com.example.eventbooking.dto.UserRequestDTO;
import com.example.eventbooking.dto.UserResponseDTO;
import com.example.eventbooking.exception.CustomException;
import com.example.eventbooking.service.UserService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserService userService;
    private final JwtUtil jwtUtil;

    // Constructor Injection
    public AuthController(UserService userService, JwtUtil jwtUtil) {
        this.userService = userService;
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/register")
    public UserResponseDTO register(@Valid @RequestBody UserRequestDTO request) {
        return userService.register(request);
    }

    @PostMapping("/login")
    public String login(@RequestParam String email,
            @RequestParam String password) {

        UserResponseDTO user = userService.login(email, password);

        if (user == null) {
            throw new CustomException("Invalid credentials");
        }

        return jwtUtil.generateToken(user.getEmail(), user.getRole());
    }
}