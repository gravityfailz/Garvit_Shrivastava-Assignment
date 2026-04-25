package com.example.eventbooking.service;

import com.example.eventbooking.dto.EventRequestDTO;
import com.example.eventbooking.dto.EventResponseDTO;

import java.util.List;

public interface EventService {

    EventResponseDTO createEvent(EventRequestDTO request);

    EventResponseDTO updateEvent(Long id, EventRequestDTO request);

    List<EventResponseDTO> getAllEvents();

    List<EventResponseDTO> getUpcomingEvents();

    List<EventResponseDTO> getPastEvents();

    List<EventResponseDTO> getCancelledEvents();

    EventResponseDTO getEventById(Long id);
}