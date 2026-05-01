package com.example.eventbooking.dto;

import java.time.LocalDateTime;

public class EventResponseDTO {

    private Long id;
    private String name;
    private String description;
    private String venue;
    private LocalDateTime eventDate;
    private int availableSeats;
    private double price;
    private String imageUrl;

    public EventResponseDTO(Long id, String name, String description, String venue,
            LocalDateTime eventDate, int availableSeats,
            double price, String imageUrl) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.venue = venue;
        this.eventDate = eventDate;
        this.availableSeats = availableSeats;
        this.price = price;
        this.imageUrl = imageUrl;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
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

    public String getImageUrl() {
        return imageUrl;
    }
}