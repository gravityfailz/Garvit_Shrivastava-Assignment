package com.example.eventbooking.service;

import com.example.eventbooking.dto.EventRequestDTO;
import com.example.eventbooking.dto.EventResponseDTO;

public interface EventService {

    EventResponseDTO createEvent(EventRequestDTO request);

    EventResponseDTO updateEvent(Long id, EventRequestDTO request);
}