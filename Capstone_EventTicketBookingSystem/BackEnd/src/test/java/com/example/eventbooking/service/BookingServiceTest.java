package com.example.eventbooking.service;

import com.example.eventbooking.dto.BookingRequestDTO;
import com.example.eventbooking.dto.BookingResponseDTO;
import com.example.eventbooking.entity.*;
import com.example.eventbooking.exception.CustomException;
import com.example.eventbooking.repository.*;
import com.example.eventbooking.service.impl.BookingServiceImpl;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class BookingServiceTest {

        private final BookingRepository bookingRepository = mock(BookingRepository.class);
        private final EventRepository eventRepository = mock(EventRepository.class);
        private final UserRepository userRepository = mock(UserRepository.class);

        private final BookingService bookingService = new BookingServiceImpl(bookingRepository, eventRepository,
                        userRepository);

        @Test
        void testBookTickets_success() {

                User user = new User();
                user.setEmail("test@gmail.com");

                Event event = new Event();
                event.setId(1L);
                event.setAvailableSeats(10);
                event.setEventDate(LocalDateTime.now().plusDays(1));

                BookingRequestDTO request = new BookingRequestDTO();
                request.setEventId(1L);
                request.setNumberOfTickets(2);

                when(userRepository.findByEmail("test@gmail.com"))
                                .thenReturn(Optional.of(user));

                when(eventRepository.findById(1L))
                                .thenReturn(Optional.of(event));

                when(bookingRepository.save(any()))
                                .thenAnswer(i -> i.getArgument(0));

                BookingResponseDTO response = bookingService.bookTickets("test@gmail.com", request);

                assertEquals("CONFIRMED", response.getStatus());
                assertEquals(8, event.getAvailableSeats());
        }

        @Test
        void testBookTickets_overCapacity() {

                User user = new User();
                user.setEmail("test@gmail.com");

                Event event = new Event();
                event.setAvailableSeats(1);
                event.setEventDate(LocalDateTime.now().plusDays(1));

                BookingRequestDTO request = new BookingRequestDTO();
                request.setEventId(1L);
                request.setNumberOfTickets(5);

                when(userRepository.findByEmail("test@gmail.com"))
                                .thenReturn(Optional.of(user));

                when(eventRepository.findById(1L))
                                .thenReturn(Optional.of(event));

                assertThrows(CustomException.class,
                                () -> bookingService.bookTickets("test@gmail.com", request));
        }

        @Test
        void testBookTickets_pastEvent() {

                User user = new User();
                user.setEmail("test@gmail.com");

                Event event = new Event();
                event.setAvailableSeats(10);
                event.setEventDate(LocalDateTime.now().minusDays(1));

                BookingRequestDTO request = new BookingRequestDTO();
                request.setEventId(1L);
                request.setNumberOfTickets(2);

                when(userRepository.findByEmail("test@gmail.com"))
                                .thenReturn(Optional.of(user));

                when(eventRepository.findById(1L))
                                .thenReturn(Optional.of(event));

                assertThrows(CustomException.class,
                                () -> bookingService.bookTickets("test@gmail.com", request));
        }

        @Test
        void testCancelBooking_success() {

                Booking booking = new Booking();
                booking.setStatus(Booking.Status.CONFIRMED);

                Event event = new Event();
                event.setEventDate(LocalDateTime.now().plusDays(1));
                event.setAvailableSeats(5);

                booking.setEvent(event);
                booking.setNumberOfTickets(2);

                when(bookingRepository.findById(1L))
                                .thenReturn(Optional.of(booking));

                assertDoesNotThrow(() -> bookingService.cancelBooking(1L));
        }

        @Test
        void testCancelBooking_within3Hours() {

                Booking booking = new Booking();
                booking.setStatus(Booking.Status.CONFIRMED);

                Event event = new Event();
                event.setEventDate(LocalDateTime.now().plusHours(2));

                booking.setEvent(event);

                when(bookingRepository.findById(1L))
                                .thenReturn(Optional.of(booking));

                assertThrows(CustomException.class,
                                () -> bookingService.cancelBooking(1L));
        }
}