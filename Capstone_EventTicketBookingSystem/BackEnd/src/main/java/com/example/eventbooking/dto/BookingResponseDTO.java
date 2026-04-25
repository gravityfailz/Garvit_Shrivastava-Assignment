package com.example.eventbooking.dto;

import java.time.LocalDateTime;

public class BookingResponseDTO {

    private Long bookingId;
    private String eventName;
    private int tickets;
    private String status;
    private LocalDateTime bookingTime;

    public BookingResponseDTO(Long bookingId, String eventName,
            int tickets, String status,
            LocalDateTime bookingTime) {
        this.bookingId = bookingId;
        this.eventName = eventName;
        this.tickets = tickets;
        this.status = status;
        this.bookingTime = bookingTime;
    }

    public Long getBookingId() {
        return bookingId;
    }

    public String getEventName() {
        return eventName;
    }

    public int getTickets() {
        return tickets;
    }

    public String getStatus() {
        return status;
    }

    public LocalDateTime getBookingTime() {
        return bookingTime;
    }
}