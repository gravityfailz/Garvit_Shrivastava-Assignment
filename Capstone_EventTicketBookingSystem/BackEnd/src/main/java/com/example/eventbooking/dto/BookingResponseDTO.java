package com.example.eventbooking.dto;

import java.time.LocalDateTime;

public class BookingResponseDTO {

    private Long id; // ✅ fixed
    private String eventName;
    private int numberOfTickets; // ✅ must exist
    private String status;
    private LocalDateTime bookingTime;

    // Constructor
    public BookingResponseDTO(Long id, String eventName, int numberOfTickets, String status,
            LocalDateTime bookingTime) {
        this.id = id;
        this.eventName = eventName;
        this.numberOfTickets = numberOfTickets;
        this.status = status;
        this.bookingTime = bookingTime;
    }

    // Getters
    public Long getId() {
        return id;
    }

    public String getEventName() {
        return eventName;
    }

    public int getNumberOfTickets() {
        return numberOfTickets;
    }

    public String getStatus() {
        return status;
    }

    public LocalDateTime getBookingTime() {
        return bookingTime;
    }
}