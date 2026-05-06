package com.example.eventbooking.config;

import jakarta.servlet.FilterChain;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.mockito.Mockito.*;

public class JwtFilterTest {

    private JwtUtil jwtUtil;
    private CustomUserDetailsService userDetailsService;
    private JwtFilter jwtFilter;

    @BeforeEach
    void setup() {
        jwtUtil = new JwtUtil();
        userDetailsService = mock(CustomUserDetailsService.class);
        jwtFilter = new JwtFilter(jwtUtil, userDetailsService);
    }

    @Test
    void testDoFilterInternal_validToken() throws Exception {
        String token = jwtUtil.generateToken("test@gmail.com", "CUSTOMER");

        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        FilterChain filterChain = mock(FilterChain.class);

        when(request.getHeader("Authorization")).thenReturn("Bearer " + token);

        UserDetails userDetails = new User(
                "test@gmail.com", "password", Collections.emptyList());
        when(userDetailsService.loadUserByUsername("test@gmail.com"))
                .thenReturn(userDetails);

        assertDoesNotThrow(() -> jwtFilter.doFilterInternal(request, response, filterChain));

        verify(filterChain).doFilter(request, response);
    }

    @Test
    void testDoFilterInternal_noAuthHeader() throws Exception {
        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        FilterChain filterChain = mock(FilterChain.class);

        when(request.getHeader("Authorization")).thenReturn(null);

        assertDoesNotThrow(() -> jwtFilter.doFilterInternal(request, response, filterChain));

        verify(filterChain).doFilter(request, response);
    }

    @Test
    void testDoFilterInternal_invalidToken() throws Exception {
        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        FilterChain filterChain = mock(FilterChain.class);

        when(request.getHeader("Authorization")).thenReturn("Bearer invalid.token.here");

        assertDoesNotThrow(() -> jwtFilter.doFilterInternal(request, response, filterChain));

        verify(filterChain).doFilter(request, response);
    }

    @Test
    void testDoFilterInternal_noBearer() throws Exception {
        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        FilterChain filterChain = mock(FilterChain.class);

        when(request.getHeader("Authorization")).thenReturn("Basic sometoken");

        assertDoesNotThrow(() -> jwtFilter.doFilterInternal(request, response, filterChain));

        verify(filterChain).doFilter(request, response);
    }

    @Test
    void testDoFilterInternal_validToken_organizer() throws Exception {
        String token = jwtUtil.generateToken("org@gmail.com", "ORGANIZER");

        HttpServletRequest request = mock(HttpServletRequest.class);
        HttpServletResponse response = mock(HttpServletResponse.class);
        FilterChain filterChain = mock(FilterChain.class);

        when(request.getHeader("Authorization")).thenReturn("Bearer " + token);

        UserDetails userDetails = new User(
                "org@gmail.com", "pass", Collections.emptyList());
        when(userDetailsService.loadUserByUsername("org@gmail.com"))
                .thenReturn(userDetails);

        assertDoesNotThrow(() -> jwtFilter.doFilterInternal(request, response, filterChain));

        verify(filterChain).doFilter(request, response);
    }
}