package com.example.eventbooking.controller;

import com.example.eventbooking.dto.EventRequestDTO;
import com.example.eventbooking.dto.EventResponseDTO;
import com.example.eventbooking.service.EventService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/events")
public class EventController {

    private final EventService eventService;

    public EventController(EventService eventService) {
        this.eventService = eventService;
    }

    @PostMapping
    public EventResponseDTO createEvent(@Valid @RequestBody EventRequestDTO request) {
        return eventService.createEvent(request);
    }

    @PutMapping("/{id}")
    public EventResponseDTO updateEvent(@PathVariable Long id,
            @Valid @RequestBody EventRequestDTO request) {
        return eventService.updateEvent(id, request);
    }

    @GetMapping
    public List<EventResponseDTO> getAllEvents() {
        return eventService.getAllEvents();
    }

    @GetMapping("/upcoming")
    public List<EventResponseDTO> getUpcomingEvents() {
        return eventService.getUpcomingEvents();
    }

    @GetMapping("/past")
    public List<EventResponseDTO> getPastEvents() {
        return eventService.getPastEvents();
    }

    @GetMapping("/cancelled")
    public List<EventResponseDTO> getCancelledEvents() {
        return eventService.getCancelledEvents();
    }

    @GetMapping("/{id}")
    public EventResponseDTO getEventById(@PathVariable Long id) {
        return eventService.getEventById(id);
    }

}