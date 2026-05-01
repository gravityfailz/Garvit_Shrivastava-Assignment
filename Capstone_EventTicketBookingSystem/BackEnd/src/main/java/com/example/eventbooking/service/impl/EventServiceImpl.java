package com.example.eventbooking.service.impl;

import com.example.eventbooking.dto.EventRequestDTO;
import com.example.eventbooking.dto.EventResponseDTO;
import com.example.eventbooking.entity.Event;
import com.example.eventbooking.entity.User;
import com.example.eventbooking.exception.CustomException;
import com.example.eventbooking.repository.EventRepository;
import com.example.eventbooking.repository.BookingRepository;
import com.example.eventbooking.repository.UserRepository;
import com.example.eventbooking.service.EventService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.security.core.context.SecurityContextHolder;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class EventServiceImpl implements EventService {

    private final EventRepository eventRepository;
    private final BookingRepository bookingRepository;
    private final UserRepository userRepository;

    public EventServiceImpl(EventRepository eventRepository,
            BookingRepository bookingRepository,
            UserRepository userRepository) {
        this.eventRepository = eventRepository;
        this.bookingRepository = bookingRepository;
        this.userRepository = userRepository;
    }

    @Override
    public EventResponseDTO createEvent(EventRequestDTO request) {
        String email = SecurityContextHolder.getContext().getAuthentication().getName();

        if (email == null || email.equals("anonymousUser")) {
            throw new CustomException("Unauthorized: No user found");
        }

        User organizer = userRepository.findByEmail(email)
                .orElseThrow(() -> new CustomException("User not found"));

        Event event = new Event();
        event.setOrganizer(organizer);
        event.setName(request.getName());
        event.setDescription(request.getDescription());
        event.setVenue(request.getVenue());
        event.setEventDate(request.getEventDate());
        event.setTotalSeats(request.getTotalSeats());
        event.setAvailableSeats(request.getTotalSeats());
        event.setPrice(request.getPrice());
        event.setCancelled(false);
        event.setImageUrl(request.getImageUrl());
        event.setOrganizer(organizer);

        Event saved = eventRepository.save(event);

        return mapToDTO(saved);
    }

    @Override
    public void deleteEvent(Long id) {

        Event event = eventRepository.findById(id)
                .orElseThrow(() -> new CustomException("Event not found"));

        bookingRepository.deleteByEventId(id);

        eventRepository.delete(event);
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
        event.setImageUrl(request.getImageUrl());

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

    @Override
    public List<EventResponseDTO> getUpcomingEvents() {

        return eventRepository.findAll().stream()
                .filter(e -> e.getEventDate().isAfter(LocalDateTime.now()) && !e.isCancelled())
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<EventResponseDTO> getPastEvents() {

        return eventRepository.findAll().stream()
                .filter(e -> e.getEventDate().isBefore(LocalDateTime.now()) && !e.isCancelled())
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    @Override
    public List<EventResponseDTO> getCancelledEvents() {

        return eventRepository.findAll().stream()
                .filter(Event::isCancelled)
                .map(this::mapToDTO)
                .collect(Collectors.toList());
    }

    private EventResponseDTO mapToDTO(Event event) {
        return new EventResponseDTO(
                event.getId(),
                event.getName(),
                event.getDescription(),
                event.getVenue(),
                event.getEventDate(),
                event.getAvailableSeats(),
                event.getPrice(),
                event.getImageUrl());
    }
}