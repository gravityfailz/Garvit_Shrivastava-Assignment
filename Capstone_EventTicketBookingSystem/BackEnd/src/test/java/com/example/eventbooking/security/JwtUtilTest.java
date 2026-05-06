package com.example.eventbooking.config;

import org.junit.jupiter.api.Test;
import com.example.eventbooking.config.JwtUtil;
import static org.junit.jupiter.api.Assertions.*;

public class JwtUtilTest {

    private final JwtUtil jwtUtil = new JwtUtil();

    @Test
    void testGenerateAndExtractEmail() {
        String token = jwtUtil.generateToken("test@gmail.com", "CUSTOMER");
        assertEquals("test@gmail.com", jwtUtil.extractEmail(token));
    }

    @Test
    void testValidateToken_valid() {
        String token = jwtUtil.generateToken("test@gmail.com", "CUSTOMER");
        assertTrue(jwtUtil.validateToken(token));
    }

    @Test
    void testValidateToken_invalid() {
        assertFalse(jwtUtil.validateToken("invalid.token.string"));
    }

    @Test
    void testGenerateToken_notNull() {
        String token = jwtUtil.generateToken("abc@gmail.com", "USER");
        assertNotNull(token);
    }

    @Test
    void testExtractEmail_differentUser() {
        String token = jwtUtil.generateToken("abc@gmail.com", "USER");
        assertEquals("abc@gmail.com", jwtUtil.extractEmail(token));
    }

    @Test
    void testValidateToken_malformedToken() {
        assertFalse(jwtUtil.validateToken("abc.invalid.token"));
    }

    @Test
    void testTokenUniqueness() {
        String token1 = jwtUtil.generateToken("a@gmail.com", "USER");
        String token2 = jwtUtil.generateToken("b@gmail.com", "USER");
        assertNotEquals(token1, token2);
    }

    @Test
    void testValidateToken_emptyString() {
        assertFalse(jwtUtil.validateToken(""));
    }

    @Test
    void testGenerateToken_organizerRole() {
        String token = jwtUtil.generateToken("org@gmail.com", "ORGANIZER");
        assertNotNull(token);
        assertTrue(jwtUtil.validateToken(token));
        assertEquals("org@gmail.com", jwtUtil.extractEmail(token));
    }

    @Test
    void testExtractEmail_afterMultipleGenerations() {
        jwtUtil.generateToken("first@gmail.com", "USER");
        String token = jwtUtil.generateToken("second@gmail.com", "CUSTOMER");
        assertEquals("second@gmail.com", jwtUtil.extractEmail(token));
    }
}