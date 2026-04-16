package com.example.session3.repository;

import com.example.session3.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

@Repository
public class UserRepository {

    private final List<User> users = new ArrayList<>();

    public UserRepository() {
        users.add(new User(1L, "Priya", 25, "USER"));
        users.add(new User(2L, "Amit", 30, "ADMIN"));
        users.add(new User(3L, "Rahul", 30, "USER"));
        users.add(new User(4L, "Neha", 28, "USER"));
        users.add(new User(5L, "Suresh", 35, "ADMIN"));
        users.add(new User(6L, "Ankit", 22, "USER"));
    }

    public List<User> findAll() {
        return users;
    }

    public void deleteById(Long id) {
        users.removeIf(user -> user.getId().equals(id));
    }
}