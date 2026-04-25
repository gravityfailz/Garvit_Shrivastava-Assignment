package com.example.eventbooking.controller;

import com.example.eventbooking.dto.*;
import com.example.eventbooking.service.BookingService;
import jakarta.validation.Valid;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/bookings")
public class BookingController {

    private final BookingService bookingService;

    public BookingController(BookingService bookingService) {
        this.bookingService = bookingService;
    }

    @PostMapping
    public BookingResponseDTO bookTickets(@Valid @RequestBody BookingRequestDTO request,
            Authentication authentication) {

        String email = authentication.getName();

        return bookingService.bookTickets(email, request);
    }

    @DeleteMapping("/{id}")
    public String cancelBooking(@PathVariable Long id) {
        bookingService.cancelBooking(id);
        return "Booking cancelled successfully";
    }
}