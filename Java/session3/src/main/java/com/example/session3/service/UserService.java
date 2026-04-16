package com.example.session3.service;

import com.example.session3.model.User;
import com.example.session3.repository.UserRepository;
import com.example.session3.exception.BadRequestException;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserService {

    private final UserRepository userRepository;

    // ✅ Constructor Injection
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> searchUsers(String name, Integer age, String role) {

        List<User> users = userRepository.findAll();

        return users.stream()
                .filter(user -> name == null || user.getName().equalsIgnoreCase(name))
                .filter(user -> age == null || user.getAge().equals(age))
                .filter(user -> role == null || user.getRole().equalsIgnoreCase(role))
                .collect(Collectors.toList());
    }

    public void deleteUser(Long id, boolean confirm) {
        if (!confirm) {
            throw new BadRequestException("Confirmation required");
        }
        userRepository.deleteById(id);
    }
}