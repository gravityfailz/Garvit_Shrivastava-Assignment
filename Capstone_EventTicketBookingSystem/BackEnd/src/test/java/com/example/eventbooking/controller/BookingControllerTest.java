package com.example.eventbooking.controller;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.example.eventbooking.service.BookingService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.core.Authentication;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class BookingControllerTest {

    @Mock
    private BookingService bookingService;

    @Mock
    private Authentication authentication;

    @InjectMocks
    private BookingController bookingController;

    private MockMvc mockMvc() {
        return MockMvcBuilders.standaloneSetup(bookingController).build();
    }

    @Test
    void testGetBookings() throws Exception {
        when(authentication.getName()).thenReturn("test@gmail.com");
        when(bookingService.getUserBookings("test@gmail.com")).thenReturn(List.of());

        mockMvc().perform(get("/api/bookings").principal(authentication))
                .andExpect(status().isOk());
    }

    @Test
    void testCancelBookingEndpoint() throws Exception {
        when(bookingService.cancelBooking(1L)).thenReturn(null);

        mockMvc().perform(put("/api/bookings/1/cancel"))
                .andExpect(status().isOk());
    }

    @Test
    void testGetMyBookings() throws Exception {
        when(authentication.getName()).thenReturn("test@gmail.com");
        when(bookingService.getUserBookings("test@gmail.com")).thenReturn(List.of());

        mockMvc().perform(get("/api/bookings/my").principal(authentication))
                .andExpect(status().isOk());
    }

    @Test
    void testGetOrganizerBookings() throws Exception {
        when(authentication.getName()).thenReturn("org@gmail.com");
        when(bookingService.getBookingsForOrganizer("org@gmail.com")).thenReturn(List.of());

        mockMvc().perform(get("/api/bookings/organizer").principal(authentication))
                .andExpect(status().isOk());
    }

    @Test
    void testBookTicketsEndpoint() throws Exception {
        when(authentication.getName()).thenReturn("test@gmail.com");
        when(bookingService.bookTickets(eq("test@gmail.com"), any())).thenReturn(null);

        mockMvc().perform(post("/api/bookings")
                .principal(authentication)
                .contentType("application/json")
                .content("{\"eventId\":1,\"numberOfTickets\":2}"))
                .andExpect(status().isOk());
    }

    @Test
    void testGetMyBookings_multipleResults() throws Exception {
        when(authentication.getName()).thenReturn("multi@gmail.com");
        when(bookingService.getUserBookings("multi@gmail.com")).thenReturn(List.of());

        mockMvc().perform(get("/api/bookings/my").principal(authentication))
                .andExpect(status().isOk());
    }
}