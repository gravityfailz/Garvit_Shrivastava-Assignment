package com.example.eventbooking.service;

import com.example.eventbooking.dto.EventRequestDTO;
import com.example.eventbooking.dto.EventResponseDTO;
import com.example.eventbooking.entity.Event;
import com.example.eventbooking.entity.User;
import com.example.eventbooking.exception.CustomException;
import com.example.eventbooking.repository.EventRepository;
import com.example.eventbooking.repository.BookingRepository;
import com.example.eventbooking.repository.UserRepository;
import com.example.eventbooking.service.impl.EventServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

public class EventServiceTest {

    private EventRepository eventRepository;
    private BookingRepository bookingRepository;
    private UserRepository userRepository;
    private EventService eventService;

    @BeforeEach
    void setup() {
        eventRepository = mock(EventRepository.class);
        bookingRepository = mock(BookingRepository.class);
        userRepository = mock(UserRepository.class);
        eventService = new EventServiceImpl(eventRepository, bookingRepository, userRepository);

        SecurityContext securityContext = mock(SecurityContext.class);
        Authentication authentication = mock(Authentication.class);
        when(authentication.getName()).thenReturn("test@gmail.com");
        when(securityContext.getAuthentication()).thenReturn(authentication);
        SecurityContextHolder.setContext(securityContext);
    }

    @Test
    void testCreateEvent_success() {
        User user = new User();
        user.setEmail("test@gmail.com");

        when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.of(user));

        EventRequestDTO request = new EventRequestDTO();
        request.setName("Concert");
        request.setDescription("Music Event");
        request.setVenue("Delhi");
        request.setEventDate(LocalDateTime.now().plusDays(5));
        request.setTotalSeats(100);
        request.setPrice(500);
        request.setImageUrl("test.jpg");

        when(eventRepository.save(any(Event.class))).thenAnswer(i -> {
            Event e = i.getArgument(0);
            e.setId(1L);
            return e;
        });

        EventResponseDTO response = eventService.createEvent(request);

        assertEquals("Concert", response.getName());
        assertEquals(100, response.getAvailableSeats());
    }

    @Test
    void testCreateEvent_userNotFound() {
        when(userRepository.findByEmail("test@gmail.com")).thenReturn(Optional.empty());
        assertThrows(CustomException.class, () -> eventService.createEvent(new EventRequestDTO()));
    }

    @Test
    void testGetEvent_notFound() {
        when(eventRepository.findById(1L)).thenReturn(Optional.empty());
        assertThrows(CustomException.class, () -> eventService.getEventById(1L));
    }

    @Test
    void testGetEventById_success() {
        Event e = new Event();
        e.setId(1L);
        e.setName("Jazz Night");
        e.setEventDate(LocalDateTime.now().plusDays(3));

        when(eventRepository.findById(1L)).thenReturn(Optional.of(e));

        EventResponseDTO response = eventService.getEventById(1L);
        assertNotNull(response);
        assertEquals("Jazz Night", response.getName());
    }

    @Test
    void testUpcomingEvents() {
        Event e = new Event();
        e.setEventDate(LocalDateTime.now().plusDays(2));
        e.setCancelled(false);

        when(eventRepository.findAll()).thenReturn(List.of(e));
        assertEquals(1, eventService.getUpcomingEvents().size());
    }

    @Test
    void testUpcomingEvents_excludesCancelled() {
        Event cancelled = new Event();
        cancelled.setEventDate(LocalDateTime.now().plusDays(1));
        cancelled.setCancelled(true);

        when(eventRepository.findAll()).thenReturn(List.of(cancelled));
        assertEquals(0, eventService.getUpcomingEvents().size());
    }

    @Test
    void testGetAllEvents() {
        when(eventRepository.findAll()).thenReturn(List.of(new Event()));
        assertEquals(1, eventService.getAllEvents().size());
    }

    @Test
    void testGetAllEvents_empty() {
        when(eventRepository.findAll()).thenReturn(List.of());
        assertEquals(0, eventService.getAllEvents().size());
    }

    @Test
    void testDeleteEvent() {
        Event e = new Event();
        e.setId(1L);
        when(eventRepository.findById(1L)).thenReturn(Optional.of(e));
        assertDoesNotThrow(() -> eventService.deleteEvent(1L));
    }

    @Test
    void testDeleteEvent_notFound() {
        when(eventRepository.findById(1L)).thenReturn(Optional.empty());
        assertThrows(CustomException.class, () -> eventService.deleteEvent(1L));
    }

    @Test
    void testPastEvents() {
        Event e = new Event();
        e.setEventDate(LocalDateTime.now().minusDays(1));
        e.setCancelled(false);

        when(eventRepository.findAll()).thenReturn(List.of(e));
        assertEquals(1, eventService.getPastEvents().size());
    }

    @Test
    void testCancelledEvents() {
        Event e = new Event();
        e.setCancelled(true);

        when(eventRepository.findAll()).thenReturn(List.of(e));
        assertEquals(1, eventService.getCancelledEvents().size());
    }

    @Test
    void testUpdateEvent() {
        Event e = new Event();
        e.setId(1L);

        when(eventRepository.findById(1L)).thenReturn(Optional.of(e));
        when(eventRepository.save(any())).thenReturn(e);

        EventRequestDTO req = new EventRequestDTO();
        req.setName("Updated");

        assertNotNull(eventService.updateEvent(1L, req));
    }

    @Test
    void testUpdateEvent_notFound() {
        when(eventRepository.findById(99L)).thenReturn(Optional.empty());
        assertThrows(CustomException.class, () -> eventService.updateEvent(99L, new EventRequestDTO()));
    }
}