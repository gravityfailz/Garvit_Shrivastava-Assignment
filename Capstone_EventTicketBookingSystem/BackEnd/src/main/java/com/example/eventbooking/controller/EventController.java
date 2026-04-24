package com.example.eventbooking.controller;

import com.example.eventbooking.dto.EventRequestDTO;
import com.example.eventbooking.dto.EventResponseDTO;
import com.example.eventbooking.service.EventService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

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
}