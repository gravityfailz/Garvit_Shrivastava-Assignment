package com.example.eventbooking.service;

import com.example.eventbooking.dto.BookingRequestDTO;
import com.example.eventbooking.dto.BookingResponseDTO;
import java.util.List;

public interface BookingService {

    BookingResponseDTO bookTickets(String userEmail, BookingRequestDTO request);

    BookingResponseDTO cancelBooking(Long id);

    List<BookingResponseDTO> getUserBookings(String email);

    List<BookingResponseDTO> getBookingsForOrganizer(String email);

}