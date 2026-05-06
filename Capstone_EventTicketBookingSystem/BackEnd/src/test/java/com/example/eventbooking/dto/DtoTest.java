package com.example.eventbooking.dto;

import org.junit.jupiter.api.Test;
import java.time.LocalDateTime;
import static org.junit.jupiter.api.Assertions.*;

public class DtoTest {

    @Test
    void testEventResponseDTO() {
        LocalDateTime date = LocalDateTime.now();
        EventResponseDTO dto = new EventResponseDTO(
                1L, "Concert", "Music Event", "Delhi",
                date, 100, 500.0, "image.jpg");

        assertEquals(1L, dto.getId());
        assertEquals("Concert", dto.getName());
        assertEquals("Music Event", dto.getDescription());
        assertEquals("Delhi", dto.getVenue());
        assertEquals(date, dto.getEventDate());
        assertEquals(100, dto.getAvailableSeats());
        assertEquals(500.0, dto.getPrice());
        assertEquals("image.jpg", dto.getImageUrl());
    }

    @Test
    void testBookingResponseDTO() {
        BookingResponseDTO dto = new BookingResponseDTO();
        dto.setEventName("Concert");
        dto.setUserEmail("test@gmail.com");
        dto.setNumberOfTickets(2);
        dto.setStatus("CONFIRMED");

        assertEquals("Concert", dto.getEventName());
        assertEquals("test@gmail.com", dto.getUserEmail());
        assertEquals(2, dto.getNumberOfTickets());
        assertEquals("CONFIRMED", dto.getStatus());
    }

    @Test
    void testBookingResponseDTO_id() {
        BookingResponseDTO dto = new BookingResponseDTO();
        dto.setId(42L);
        assertEquals(42L, dto.getId());
    }

    @Test
    void testEventRequestDTO_settersAndGetters() {
        EventRequestDTO dto = new EventRequestDTO();
        LocalDateTime date = LocalDateTime.now().plusDays(5);

        dto.setName("Rock Night");
        dto.setDescription("Rock music");
        dto.setVenue("Mumbai");
        dto.setEventDate(date);
        dto.setTotalSeats(200);
        dto.setPrice(999.0);
        dto.setImageUrl("rock.jpg");

        assertEquals("Rock Night", dto.getName());
        assertEquals("Rock music", dto.getDescription());
        assertEquals("Mumbai", dto.getVenue());
        assertEquals(date, dto.getEventDate());
        assertEquals(200, dto.getTotalSeats());
        assertEquals(999.0, dto.getPrice());
        assertEquals("rock.jpg", dto.getImageUrl());
    }

    @Test
    void testBookingRequestDTO_settersAndGetters() {
        BookingRequestDTO dto = new BookingRequestDTO();
        dto.setEventId(5L);
        dto.setNumberOfTickets(3);

        assertEquals(5L, dto.getEventId());
        assertEquals(3, dto.getNumberOfTickets());
    }

    @Test
    void testBookingResponseDTO_cancelledStatus() {
        BookingResponseDTO dto = new BookingResponseDTO();
        dto.setStatus("CANCELLED");
        assertEquals("CANCELLED", dto.getStatus());
    }

    @Test
    void testEventResponseDTO_differentValues() {
        LocalDateTime date = LocalDateTime.now().plusDays(10);
        EventResponseDTO dto = new EventResponseDTO(
                2L, "Fest", "Fun Event", "Pune",
                date, 50, 100.0, "fest.jpg");

        assertEquals(2L, dto.getId());
        assertEquals("Fest", dto.getName());
        assertEquals(50, dto.getAvailableSeats());
        assertEquals(100.0, dto.getPrice());
    }

    @Test
    void testUserRequestDTO() {
        UserRequestDTO dto = new UserRequestDTO();
        dto.setEmail("user@gmail.com");
        dto.setPassword("pass123");

        assertEquals("user@gmail.com", dto.getEmail());
        assertEquals("pass123", dto.getPassword());
    }

    @Test
    void testUserResponseDTO_notNull() {
        // UserResponseDTO uses all-args constructor: (Long, String, String, String,
        // String)
        UserResponseDTO dto = new UserResponseDTO(1L, "user@gmail.com", "User", "CUSTOMER", "jwt-token");
        assertNotNull(dto);
    }

    @Test
    void testUserResponseDTO_secondVariant() {
        UserResponseDTO dto = new UserResponseDTO(2L, "org@gmail.com", "Organizer", "ORGANIZER", "jwt-token-2");
        assertNotNull(dto);
    }
}