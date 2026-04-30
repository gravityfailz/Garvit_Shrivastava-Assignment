package com.example.eventbooking.service;

import com.example.eventbooking.dto.UserRequestDTO;
import com.example.eventbooking.dto.UserResponseDTO;

public interface UserService {
    UserResponseDTO register(UserRequestDTO request);

    UserResponseDTO login(String email, String password);
}