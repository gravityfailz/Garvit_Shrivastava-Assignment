package com.example.eventbooking.service.impl;

import com.example.eventbooking.dto.UserRequestDTO;
import com.example.eventbooking.dto.UserResponseDTO;
import com.example.eventbooking.entity.User;
import com.example.eventbooking.exception.CustomException;
import com.example.eventbooking.repository.UserRepository;
import com.example.eventbooking.service.UserService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final BCryptPasswordEncoder passwordEncoder;

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
        this.passwordEncoder = new BCryptPasswordEncoder();
    }

    @Override
    public UserResponseDTO register(UserRequestDTO request) {

        if (userRepository.findByEmail(request.getEmail()).isPresent()) {
            throw new CustomException("Email already exists");
        }

        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setPhone(request.getPhone());
        user.setRole(User.Role.valueOf(request.getRole().toUpperCase()));

        User saved = userRepository.save(user);

        return new UserResponseDTO(
                saved.getId(),
                saved.getName(),
                saved.getEmail(),
                saved.getPhone(),
                saved.getRole().name());
    }

    @Override
    public UserResponseDTO login(String email, String password) {

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new CustomException("Invalid credentials"));

        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new CustomException("Invalid credentials");
        }

        return new UserResponseDTO(
                user.getId(),
                user.getName(),
                user.getEmail(),
                user.getPhone(),
                user.getRole().name());
    }
}