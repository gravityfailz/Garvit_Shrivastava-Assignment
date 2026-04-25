package com.example.eventbooking.service;

import com.example.eventbooking.dto.BookingRequestDTO;
import com.example.eventbooking.dto.BookingResponseDTO;

public interface BookingService {

    BookingResponseDTO bookTickets(String userEmail, BookingRequestDTO request);

    void cancelBooking(Long bookingId);

    List<BookingResponseDTO> getUserBookings(String email);
}