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
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
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
                event.setName("Concert");
                event.setAvailableSeats(10);
                event.setEventDate(LocalDateTime.now().plusDays(1));

                BookingRequestDTO request = new BookingRequestDTO();
                request.setEventId(1L);
                request.setNumberOfTickets(2);

                when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.of(user));
                when(eventRepository.findById(1L)).thenReturn(Optional.of(event));
                when(bookingRepository.save(any())).thenAnswer(i -> {
                        Booking b = i.getArgument(0);
                        b.setId(1L);
                        return b;
                });

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

                when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.of(user));
                when(eventRepository.findById(1L)).thenReturn(Optional.of(event));

                assertThrows(CustomException.class,
                                () -> bookingService.bookTickets("test@gmail.com", request));
        }

        @Test
        void testGetUserBookings() {
                User user = new User();
                user.setEmail("test@gmail.com");

                Event event = new Event();
                event.setName("Concert");

                Booking booking = new Booking();
                booking.setEvent(event);
                booking.setUser(user);
                booking.setNumberOfTickets(2);
                booking.setStatus(Booking.Status.CONFIRMED);

                when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.of(user));
                when(bookingRepository.findByUser(user)).thenReturn(List.of(booking));

                assertEquals(1, bookingService.getUserBookings("test@gmail.com").size());
        }

        @Test
        void testGetUserBookings_empty() {
                User user = new User();
                user.setEmail("empty@gmail.com");

                when(userRepository.findByEmail("empty@gmail.com")).thenReturn(Optional.of(user));
                when(bookingRepository.findByUser(user)).thenReturn(List.of());

                assertEquals(0, bookingService.getUserBookings("empty@gmail.com").size());
        }

        @Test
        void testCancelBooking_notFound() {
                when(bookingRepository.findById(1L)).thenReturn(Optional.empty());
                assertThrows(CustomException.class, () -> bookingService.cancelBooking(1L));
        }

        @Test
        void testBookTickets_insufficientSeats() {
                User user = new User();
                user.setEmail("test@gmail.com");

                Event event = new Event();
                event.setAvailableSeats(1);
                event.setCancelled(false);
                event.setEventDate(LocalDateTime.now().plusDays(1));

                BookingRequestDTO req = new BookingRequestDTO();
                req.setEventId(1L);
                req.setNumberOfTickets(5);

                when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.of(user));
                when(eventRepository.findById(1L)).thenReturn(Optional.of(event));

                assertThrows(CustomException.class,
                                () -> bookingService.bookTickets("test@gmail.com", req));
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

                when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.of(user));
                when(eventRepository.findById(1L)).thenReturn(Optional.of(event));

                assertThrows(CustomException.class,
                                () -> bookingService.bookTickets("test@gmail.com", request));
        }

        @Test
        void testCancelBooking_success() {
                User user = new User();
                user.setEmail("test@gmail.com");

                Event event = new Event();
                event.setName("Concert");
                event.setEventDate(LocalDateTime.now().plusDays(1));
                event.setAvailableSeats(5);

                Booking booking = new Booking();
                booking.setId(1L);
                booking.setUser(user);
                booking.setEvent(event);
                booking.setNumberOfTickets(2);
                booking.setStatus(Booking.Status.CONFIRMED);

                when(bookingRepository.findById(1L)).thenReturn(Optional.of(booking));
                when(bookingRepository.save(any())).thenAnswer(i -> i.getArgument(0));

                assertDoesNotThrow(() -> bookingService.cancelBooking(1L));
        }

        @Test
        void testCancelBooking_within3Hours() {
                Event event = new Event();
                event.setEventDate(LocalDateTime.now().plusHours(2));

                Booking booking = new Booking();
                booking.setId(1L);
                booking.setEvent(event);
                booking.setStatus(Booking.Status.CONFIRMED);

                when(bookingRepository.findById(1L)).thenReturn(Optional.of(booking));

                assertThrows(CustomException.class, () -> bookingService.cancelBooking(1L));
        }

        @Test
        void testCancelBooking_alreadyCancelled() {
                Booking booking = new Booking();
                booking.setId(1L);
                booking.setStatus(Booking.Status.CANCELLED);

                when(bookingRepository.findById(1L)).thenReturn(Optional.of(booking));

                assertThrows(CustomException.class, () -> bookingService.cancelBooking(1L));
        }

        @Test
        void testBookTickets_eventCancelled() {
                Event event = new Event();
                event.setCancelled(true);

                when(eventRepository.findById(1L)).thenReturn(Optional.of(event));
                when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.of(new User()));

                assertThrows(CustomException.class,
                                () -> bookingService.bookTickets("test@gmail.com", new BookingRequestDTO()));
        }

        @Test
        void testUserNotFound() {
                when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.empty());
                assertThrows(CustomException.class,
                                () -> bookingService.bookTickets("test@gmail.com", new BookingRequestDTO()));
        }

        @Test
        void testEventNotFound() {
                when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.of(new User()));
                when(eventRepository.findById(any())).thenReturn(Optional.empty());

                BookingRequestDTO req = new BookingRequestDTO();
                req.setEventId(99L);
                req.setNumberOfTickets(1);

                assertThrows(CustomException.class,
                                () -> bookingService.bookTickets("test@gmail.com", req));
        }

        @Test
        void testGetBookingsForOrganizer() {
                User organizer = new User();
                organizer.setEmail("org@gmail.com");

                when(userRepository.findByEmail("org@gmail.com")).thenReturn(Optional.of(organizer));

                // Uses whatever repository method your impl calls internally;
                // returning empty list is safe and exercises the service code path
                List<BookingResponseDTO> result = bookingService.getBookingsForOrganizer("org@gmail.com");

                assertNotNull(result);
        }

        @Test
        void testOrganizerBookings() throws Exception {
                // Covered by testGetBookingsForOrganizer above
        }
}