package com.example.eventbooking.service.impl;

import com.example.eventbooking.dto.BookingRequestDTO;
import com.example.eventbooking.dto.BookingResponseDTO;
import com.example.eventbooking.entity.*;
import com.example.eventbooking.exception.CustomException;
import com.example.eventbooking.repository.*;
import com.example.eventbooking.service.BookingService;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

import java.time.LocalDateTime;

@Service
public class BookingServiceImpl implements BookingService {

    private final BookingRepository bookingRepository;
    private final EventRepository eventRepository;
    private final UserRepository userRepository;

    public BookingServiceImpl(BookingRepository bookingRepository,
            EventRepository eventRepository,
            UserRepository userRepository) {
        this.bookingRepository = bookingRepository;
        this.eventRepository = eventRepository;
        this.userRepository = userRepository;
    }

    @Override
    public BookingResponseDTO bookTickets(String userEmail, BookingRequestDTO request) {

        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new CustomException("User not found"));

        Event event = eventRepository.findById(request.getEventId())
                .orElseThrow(() -> new CustomException("Event not found"));

        if (event.isCancelled()) {
            throw new CustomException("Event is cancelled");
        }

        if (event.getAvailableSeats() < request.getNumberOfTickets()) {
            throw new CustomException("Not enough seats available");
        }

        // Deduct seats
        event.setAvailableSeats(event.getAvailableSeats() - request.getNumberOfTickets());
        eventRepository.save(event);

        Booking booking = new Booking();
        booking.setUser(user);
        booking.setEvent(event);
        booking.setNumberOfTickets(request.getNumberOfTickets());
        booking.setBookingTime(LocalDateTime.now());
        booking.setStatus(Booking.Status.CONFIRMED);

        Booking saved = bookingRepository.save(booking);

        return new BookingResponseDTO(
                saved.getId(),
                event.getName(),
                saved.getNumberOfTickets(),
                saved.getStatus().name(),
                saved.getBookingTime());
    }

    @Override
    public void cancelBooking(Long bookingId) {

        Booking booking = bookingRepository.findById(bookingId)
                .orElseThrow(() -> new CustomException("Booking not found"));

        if (booking.getStatus() == Booking.Status.CANCELLED) {
            throw new CustomException("Already cancelled");
        }

        // restore seats
        Event event = booking.getEvent();
        event.setAvailableSeats(event.getAvailableSeats() + booking.getNumberOfTickets());
        eventRepository.save(event);

        booking.setStatus(Booking.Status.CANCELLED);

        bookingRepository.save(booking);
    }

    @Override
    public List<BookingResponseDTO> getUserBookings(String email) {

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new CustomException("User not found"));

        return bookingRepository.findAll().stream()
                .filter(b -> b.getUser().getId().equals(user.getId()))
                .map(b -> new BookingResponseDTO(
                        b.getId(),
                        b.getEvent().getName(),
                        b.getNumberOfTickets(),
                        b.getStatus().name(),
                        b.getBookingTime()))
                .collect(Collectors.toList());
    }
}