package com.example.Backend.service;

import com.example.BackEnd.entity.User;
import com.example.BackEnd.repository.UserRepository;
import com.example.BackEnd.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public User register(User user) {
        return userRepository.save(user);
    }

    public String login(String email, String password) {
        Optional<User> user = userRepository.findByEmail(email);

        if (user.isPresent() && user.get().getPassword().equals(password)) {
            return JwtUtil.generateToken(email, user.get().getRole());
        }
        return null;
    }
}