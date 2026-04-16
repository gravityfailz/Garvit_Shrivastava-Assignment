package session2.src.main.java.service;

import com.example.demo.model.User;
import com.example.demo.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {

    private final UserRepository userRepository;

    // Constructor Injection (MANDATORY)
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> getUsers() {
        return userRepository.getAllUsers();
    }

    public User getUser(int id) {
        return userRepository.getUserById(id);
    }

    public String createUser(User user) {
        userRepository.addUser(user);
        return "User created successfully";
    }
}