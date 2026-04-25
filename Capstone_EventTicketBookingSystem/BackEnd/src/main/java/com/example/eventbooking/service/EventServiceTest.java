package com.example.eventbooking.service;

import com.example.eventbooking.dto.EventRequestDTO;
import com.example.eventbooking.dto.EventResponseDTO;
import com.example.eventbooking.entity.Event;
import com.example.eventbooking.repository.EventRepository;
import com.example.eventbooking.service.impl.EventServiceImpl;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class EventServiceTest {

    private final EventRepository eventRepository = mock(EventRepository.class);

    private final EventService eventService = new EventServiceImpl(eventRepository);

    @Test
    void testCreateEvent_success() {

        EventRequestDTO request = new EventRequestDTO();
        request.setName("Concert");
        request.setDescription("Music");
        request.setVenue("Delhi");
        request.setEventDate(LocalDateTime.now().plusDays(5));
        request.setTotalSeats(100);
        request.setPrice(500);

        when(eventRepository.save(any(Event.class)))
                .thenAnswer(i -> i.getArgument(0));

        EventResponseDTO response = eventService.createEvent(request);

        assertEquals("Concert", response.getName());
        assertEquals(100, response.getAvailableSeats());
    }
}