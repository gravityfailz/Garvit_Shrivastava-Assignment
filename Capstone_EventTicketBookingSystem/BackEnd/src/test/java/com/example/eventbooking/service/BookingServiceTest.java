package com.example.eventbooking.service;

import com.example.eventbooking.dto.BookingRequestDTO;
import com.example.eventbooking.dto.BookingResponseDTO;
import com.example.eventbooking.entity.*;
import com.example.eventbooking.repository.*;
import com.example.eventbooking.service.impl.BookingServiceImpl;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

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
                user.setId(1L);
                user.setEmail("test@gmail.com");

                Event event = new Event();
                event.setId(1L);
                event.setName("Concert");
                event.setAvailableSeats(10);
                event.setCancelled(false);

                BookingRequestDTO request = new BookingRequestDTO();
                request.setEventId(1L);
                request.setNumberOfTickets(2);

                when(userRepository.findByEmail("test@gmail.com"))
                                .thenReturn(Optional.of(user));

                when(eventRepository.findById(1L))
                                .thenReturn(Optional.of(event));

                when(bookingRepository.save(any(Booking.class)))
                                .thenAnswer(i -> i.getArgument(0));

                BookingResponseDTO response = bookingService.bookTickets("test@gmail.com", request);

                assertEquals("CONFIRMED", response.getStatus());
                assertEquals(8, event.getAvailableSeats());
        }
}