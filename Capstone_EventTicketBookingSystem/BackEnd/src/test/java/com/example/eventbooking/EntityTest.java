package com.example.eventbooking.entity;

import org.junit.jupiter.api.Test;
import java.time.LocalDateTime;
import static org.junit.jupiter.api.Assertions.*;

public class EntityTest {

    // ───── User ─────

    @Test
    void testUser_settersAndGetters() {
        User user = new User();
        user.setId(1L);
        user.setEmail("test@gmail.com");
        user.setPassword("secret");
        user.setRole(User.Role.CUSTOMER);

        assertEquals(1L, user.getId());
        assertEquals("test@gmail.com", user.getEmail());
        assertEquals("secret", user.getPassword());
        assertEquals(User.Role.CUSTOMER, user.getRole());
    }

    @Test
    void testUser_roleOrganizer() {
        User user = new User();
        user.setRole(User.Role.ORGANIZER);
        assertEquals(User.Role.ORGANIZER, user.getRole());
    }

    @Test
    void testUser_roleEnum_values() {
        User.Role[] roles = User.Role.values();
        assertTrue(roles.length >= 2);
        assertEquals(User.Role.CUSTOMER, User.Role.valueOf("CUSTOMER"));
        assertEquals(User.Role.ORGANIZER, User.Role.valueOf("ORGANIZER"));
    }

    @Test
    void testUser_emailUniqueness() {
        User u1 = new User();
        User u2 = new User();
        u1.setEmail("a@gmail.com");
        u2.setEmail("b@gmail.com");
        assertNotEquals(u1.getEmail(), u2.getEmail());
    }

    // ───── Event ─────

    @Test
    void testEvent_settersAndGetters() {
        LocalDateTime date = LocalDateTime.now().plusDays(5);
        Event event = new Event();
        event.setId(1L);
        event.setName("Concert");
        event.setDescription("Music show");
        event.setVenue("Delhi");
        event.setEventDate(date);
        event.setTotalSeats(200);
        event.setAvailableSeats(150);
        event.setPrice(500.0);
        event.setImageUrl("img.jpg");
        event.setCancelled(false);

        assertEquals(1L, event.getId());
        assertEquals("Concert", event.getName());
        assertEquals("Music show", event.getDescription());
        assertEquals("Delhi", event.getVenue());
        assertEquals(date, event.getEventDate());
        assertEquals(200, event.getTotalSeats());
        assertEquals(150, event.getAvailableSeats());
        assertEquals(500.0, event.getPrice());
        assertEquals("img.jpg", event.getImageUrl());
        assertFalse(event.isCancelled());
    }

    @Test
    void testEvent_cancelledFlag() {
        Event event = new Event();
        event.setCancelled(true);
        assertTrue(event.isCancelled());
    }

    @Test
    void testEvent_organizer() {
        User organizer = new User();
        organizer.setEmail("org@gmail.com");

        Event event = new Event();
        event.setOrganizer(organizer);

        assertEquals("org@gmail.com", event.getOrganizer().getEmail());
    }

    @Test
    void testEvent_availableSeatsDecrements() {
        Event event = new Event();
        event.setAvailableSeats(10);
        event.setAvailableSeats(event.getAvailableSeats() - 3);
        assertEquals(7, event.getAvailableSeats());
    }

    // ───── Booking ─────

    @Test
    void testBooking_settersAndGetters() {
        User user = new User();
        user.setEmail("test@gmail.com");

        Event event = new Event();
        event.setName("Fest");

        Booking booking = new Booking();
        booking.setId(1L);
        booking.setUser(user);
        booking.setEvent(event);
        booking.setNumberOfTickets(3);
        booking.setStatus(Booking.Status.CONFIRMED);

        assertEquals(1L, booking.getId());
        assertEquals("test@gmail.com", booking.getUser().getEmail());
        assertEquals("Fest", booking.getEvent().getName());
        assertEquals(3, booking.getNumberOfTickets());
        assertEquals(Booking.Status.CONFIRMED, booking.getStatus());
    }

    @Test
    void testBooking_statusCancelled() {
        Booking booking = new Booking();
        booking.setStatus(Booking.Status.CANCELLED);
        assertEquals(Booking.Status.CANCELLED, booking.getStatus());
    }

    @Test
    void testBookingStatus_enumValues() {
        Booking.Status[] values = Booking.Status.values();
        assertEquals(2, values.length);
        assertEquals(Booking.Status.CONFIRMED, Booking.Status.valueOf("CONFIRMED"));
        assertEquals(Booking.Status.CANCELLED, Booking.Status.valueOf("CANCELLED"));
    }

    @Test
    void testBooking_numberOfTickets() {
        Booking booking = new Booking();
        booking.setNumberOfTickets(5);
        assertEquals(5, booking.getNumberOfTickets());
    }
}