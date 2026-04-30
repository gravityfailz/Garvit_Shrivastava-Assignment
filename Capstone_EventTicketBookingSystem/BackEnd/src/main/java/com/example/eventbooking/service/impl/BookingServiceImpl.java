package com.example.eventbooking.service.impl;

import com.example.eventbooking.dto.BookingRequestDTO;
import com.example.eventbooking.dto.BookingResponseDTO;
import com.example.eventbooking.entity.*;
import com.example.eventbooking.exception.CustomException;
import com.example.eventbooking.repository.*;
import com.example.eventbooking.service.BookingService;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

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
    public List<BookingResponseDTO> getBookingsForOrganizer(String email) {
        List<Booking> bookings = bookingRepository.findByEventOrganizerEmail(email);
        return bookings.stream().map(this::mapToDTO).toList();
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

        if (event.getEventDate().isBefore(LocalDateTime.now())) {
            throw new CustomException("Cannot book tickets for past events");
        }

        if (event.getAvailableSeats() < request.getNumberOfTickets()) {
            throw new CustomException("Not enough seats available");
        }

        event.setAvailableSeats(event.getAvailableSeats() - request.getNumberOfTickets());
        eventRepository.save(event);

        Booking booking = new Booking();
        booking.setUser(user);
        booking.setEvent(event);
        booking.setNumberOfTickets(request.getNumberOfTickets());
        booking.setBookingTime(LocalDateTime.now());
        booking.setStatus(Booking.Status.CONFIRMED);

        Booking saved = bookingRepository.save(booking);

        return mapToDTO(saved);
    }

    @Override
    public BookingResponseDTO cancelBooking(Long id) {

        Booking booking = bookingRepository.findById(id)
                .orElseThrow(() -> new CustomException("Booking not found"));

        if (booking.getStatus() == Booking.Status.CANCELLED) {
            throw new CustomException("Already cancelled");
        }

        Event event = booking.getEvent();

        long hours = java.time.Duration.between(LocalDateTime.now(), event.getEventDate()).toHours();

        if (hours < 3) {
            throw new CustomException("Cannot cancel within 3 hours of event");
        }

        event.setAvailableSeats(event.getAvailableSeats() + booking.getNumberOfTickets());
        eventRepository.save(event);

        booking.setStatus(Booking.Status.CANCELLED);

        Booking saved = bookingRepository.save(booking);

        return mapToDTO(saved);
    }

    @Override
    public List<BookingResponseDTO> getUserBookings(String email) {

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new CustomException("User not found"));

        return bookingRepository.findByUser(user)
                .stream()
                .map(this::mapToDTO)
                .toList();
    }

    private BookingResponseDTO mapToDTO(Booking booking) {
        return new BookingResponseDTO(
                booking.getId(),
                booking.getEvent().getName(),
                booking.getNumberOfTickets(),
                booking.getStatus().name(),
                booking.getBookingTime());
    }
}