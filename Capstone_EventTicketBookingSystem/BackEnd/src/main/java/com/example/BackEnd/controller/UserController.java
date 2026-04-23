package com.example.BackEnd.controller;

import com.example.BackEnd.entity.User;
import com.example.BackEnd.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
@CrossOrigin
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public User register(@RequestBody User user) {
        return userService.register(user);
    }

    @PostMapping("/login")
    public String login(@RequestBody User user) {
        String token = userService.login(user.getEmail(), user.getPassword());

        if (token != null) {
            return token;
        }
        return "Invalid Credentials";
    }
}