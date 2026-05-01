package com.example.eventbooking.controller;

import com.example.eventbooking.exception.CustomException;
import com.example.eventbooking.repository.UserRepository;
import org.springframework.security.core.Authentication;
import com.example.eventbooking.entity.User;
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
    private final UserRepository userRepository;

    //
    public EventController(EventService eventService, UserRepository userRepository) {
        this.eventService = eventService;
        this.userRepository = userRepository;
    }

    @PostMapping
    public EventResponseDTO createEvent(@RequestBody EventRequestDTO request,
            Authentication authentication) {

        String email = authentication.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new CustomException("User not found"));

        if (user.getRole() != User.Role.ORGANIZER) {
            throw new CustomException("Only ORGANIZER can create events");
        }

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

    @DeleteMapping("/{id}")
    public String deleteEvent(@PathVariable Long id, Authentication auth) {

        String email = auth.getName();

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new CustomException("User not found"));

        if (user.getRole() != User.Role.ORGANIZER) {
            throw new CustomException("Only organizer can delete events");
        }

        eventService.deleteEvent(id);

        return "Event deleted successfully";
    }
}