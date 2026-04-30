package com.example.eventbooking.dto;

import java.time.LocalDateTime;

public class EventResponseDTO {

    private Long id;
    private String name;
    private String venue;
    private LocalDateTime eventDate;
    private int availableSeats;
    private double price;

    public EventResponseDTO(Long id, String name, String venue,
            LocalDateTime eventDate, int availableSeats, double price) {
        this.id = id;
        this.name = name;
        this.venue = venue;
        this.eventDate = eventDate;
        this.availableSeats = availableSeats;
        this.price = price;
        this.imageUrl = imageUrl;
    }

    // getters
    public Long getId() {
        return id;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public String getName() {
        return name;
    }

    public String getVenue() {
        return venue;
    }

    public LocalDateTime getEventDate() {
        return eventDate;
    }

    public int getAvailableSeats() {
        return availableSeats;
    }

    public double getPrice() {
        return price;
    }

    private String imageUrl;
}