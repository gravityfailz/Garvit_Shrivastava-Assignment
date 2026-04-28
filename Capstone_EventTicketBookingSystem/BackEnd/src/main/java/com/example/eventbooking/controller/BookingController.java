package com.example.eventbooking.controller;

import com.example.eventbooking.dto.*;
import com.example.eventbooking.service.BookingService;
import jakarta.validation.Valid;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import java.util.List;

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

    @GetMapping("/my")
    public List<BookingResponseDTO> getMyBookings(Authentication authentication) {

        String email = authentication.getName();

        return bookingService.getUserBookings(email);
    }

    @GetMapping
    public List<BookingResponseDTO> getUserBookings(Authentication authentication) {
        String email = authentication.getName();
        return bookingService.getUserBookings(email);
    }

    @PutMapping("/{id}/cancel")
    public BookingResponseDTO cancelBooking(@PathVariable Long id) {
        return bookingService.cancelBooking(id);
    }
}