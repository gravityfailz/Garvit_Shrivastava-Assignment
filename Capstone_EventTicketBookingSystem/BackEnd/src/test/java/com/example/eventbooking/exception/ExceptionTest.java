package com.example.eventbooking.exception;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

public class ExceptionTest {

    private final GlobalExceptionHandler handler = new GlobalExceptionHandler();

    @Test
    void testCustomException() {
        CustomException ex = new CustomException("error");
        assertEquals("error", ex.getMessage());
    }

    @Test
    void testCustomExceptionMessage() {
        CustomException ex = new CustomException("Test error");
        assertNotNull(ex);
        assertEquals("Test error", ex.getMessage());
    }

    @Test
    void testExceptionThrow() {
        assertThrows(CustomException.class, () -> {
            throw new CustomException("error");
        });
    }

    @Test
    void testGlobalExceptionHandler_customException() {
        CustomException ex = new CustomException("booking failed");
        ResponseEntity<?> response = handler.handleCustomException(ex);

        assertNotNull(response);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertNotNull(response.getBody());
    }

    @Test
    void testGlobalExceptionHandler_returnsNonNullBody() {
        CustomException ex = new CustomException("something went wrong");
        ResponseEntity<?> response = handler.handleCustomException(ex);
        assertNotNull(response.getBody());
        assertTrue(response.getBody().toString().contains("something went wrong"));
    }

    @Test
    void testCustomException_isRuntimeException() {
        CustomException ex = new CustomException("runtime check");
        assertInstanceOf(RuntimeException.class, ex);
    }

    @Test
    void testCustomException_differentMessages() {
        CustomException ex1 = new CustomException("msg1");
        CustomException ex2 = new CustomException("msg2");
        assertNotEquals(ex1.getMessage(), ex2.getMessage());
    }

    @Test
    void testCustomException_emptyMessage() {
        CustomException ex = new CustomException("");
        assertEquals("", ex.getMessage());
    }
}