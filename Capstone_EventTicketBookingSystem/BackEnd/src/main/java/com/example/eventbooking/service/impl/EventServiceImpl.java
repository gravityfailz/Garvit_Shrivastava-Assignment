package com.example.eventbooking.service.impl;

import com.example.eventbooking.dto.EventRequestDTO;
import com.example.eventbooking.dto.EventResponseDTO;
import com.example.eventbooking.entity.Event;
import com.example.eventbooking.exception.CustomException;
import com.example.eventbooking.repository.EventRepository;
import com.example.eventbooking.service.EventService;
import org.springframework.stereotype.Service;

@Service
public class EventServiceImpl implements EventService {

    private final EventRepository eventRepository;

    public EventServiceImpl(EventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }

    @Override
    public EventResponseDTO createEvent(EventRequestDTO request) {

        Event event = new Event();
        event.setName(request.getName());
        event.setDescription(request.getDescription());
        event.setVenue(request.getVenue());
        event.setEventDate(request.getEventDate());
        event.setTotalSeats(request.getTotalSeats());
        event.setAvailableSeats(request.getTotalSeats());
        event.setPrice(request.getPrice());
        event.setCancelled(false);

        Event saved = eventRepository.save(event);

        return mapToDTO(saved);
    }

    @Override
    public EventResponseDTO updateEvent(Long id, EventRequestDTO request) {

        Event event = eventRepository.findById(id)
                .orElseThrow(() -> new CustomException("Event not found"));

        event.setName(request.getName());
        event.setDescription(request.getDescription());
        event.setVenue(request.getVenue());
        event.setEventDate(request.getEventDate());
        event.setTotalSeats(request.getTotalSeats());
        event.setPrice(request.getPrice());

        Event updated = eventRepository.save(event);

        return mapToDTO(updated);
    }

    @Override
    public List<EventResponseDTO> getAllEvents() {

        return eventRepository.findAll()
                .stream()
                .map(this::mapToDTO)
                .toList();
    }

    @Override
    public EventResponseDTO getEventById(Long id) {

        Event event = eventRepository.findById(id)
                .orElseThrow(() -> new CustomException("Event not found"));

        return mapToDTO(event);
    }

    private EventResponseDTO mapToDTO(Event event) {
        return new EventResponseDTO(
                event.getId(),
                event.getName(),
                event.getVenue(),
                event.getEventDate(),
                event.getAvailableSeats(),
                event.getPrice());
    }
}