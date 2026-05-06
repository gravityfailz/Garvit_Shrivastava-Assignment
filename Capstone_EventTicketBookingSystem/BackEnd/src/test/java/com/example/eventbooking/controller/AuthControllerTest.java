package com.example.eventbooking.controller;

import com.example.eventbooking.config.JwtUtil;
import com.example.eventbooking.dto.UserResponseDTO;
import com.example.eventbooking.service.UserService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(MockitoExtension.class)
public class AuthControllerTest {

    @Mock
    private UserService userService;

    @Mock
    private JwtUtil jwtUtil;

    @InjectMocks
    private AuthController authController;

    private MockMvc mockMvc() {
        return MockMvcBuilders.standaloneSetup(authController).build();
    }

    private UserResponseDTO dummyUser() {
        return new UserResponseDTO(1L, "test@gmail.com", "Test User", "CUSTOMER", "jwt-token");
    }

    @Test
    void testRegister() throws Exception {
        when(userService.register(any())).thenReturn(dummyUser());

        mockMvc().perform(post("/api/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{" +
                        "\"name\":\"Test User\"," +
                        "\"email\":\"test@gmail.com\"," +
                        "\"password\":\"pass1234\"," +
                        "\"phone\":\"9876543210\"," +
                        "\"role\":\"CUSTOMER\"" +
                        "}"))
                .andExpect(status().isOk());
    }

    @Test
    void testRegister_organizer() throws Exception {
        when(userService.register(any())).thenReturn(
                new UserResponseDTO(2L, "org@gmail.com", "Organizer", "ORGANIZER", "jwt-token-2"));

        mockMvc().perform(post("/api/auth/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{" +
                        "\"name\":\"Org User\"," +
                        "\"email\":\"org@gmail.com\"," +
                        "\"password\":\"pass5678\"," +
                        "\"phone\":\"9123456780\"," +
                        "\"role\":\"ORGANIZER\"" +
                        "}"))
                .andExpect(status().isOk());
    }

    @Test
    void testLogin() throws Exception {
        when(userService.login(anyString(), anyString())).thenReturn(dummyUser());
        when(jwtUtil.generateToken(anyString(), anyString())).thenReturn("mocked-token");

        mockMvc().perform(post("/api/auth/login")
                .param("email", "test@gmail.com")
                .param("password", "pass1234"))
                .andExpect(status().isOk());
    }

    @Test
    void testLogin_returnsToken() throws Exception {
        when(userService.login(anyString(), anyString())).thenReturn(
                new UserResponseDTO(1L, "admin@gmail.com", "Admin", "CUSTOMER", "some-token"));
        when(jwtUtil.generateToken(anyString(), anyString()))
                .thenReturn("eyJhbGciOiJIUzI1NiJ9.test.token");

        mockMvc().perform(post("/api/auth/login")
                .param("email", "admin@gmail.com")
                .param("password", "adminpass"))
                .andExpect(status().isOk());
    }
}