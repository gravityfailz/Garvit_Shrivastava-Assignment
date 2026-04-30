package com.example.eventbooking.dto;

import java.time.LocalDateTime;

public class BookingResponseDTO {

    private Long id;
    private String eventName;
    private int numberOfTickets;
    private String status;
    private LocalDateTime bookingTime;

    public BookingResponseDTO() {
    }

    public BookingResponseDTO(Long id, String eventName, int numberOfTickets, String status,
            LocalDateTime bookingTime) {
        this.id = id;
        this.eventName = eventName;
        this.numberOfTickets = numberOfTickets;
        this.status = status;
        this.bookingTime = bookingTime;
    }

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

    public void setId(Long id) {
        this.id = id;
    }

    public void setEventName(String eventName) {
        this.eventName = eventName;
    }

    public void setNumberOfTickets(int numberOfTickets) {
        this.numberOfTickets = numberOfTickets;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public void setBookingTime(LocalDateTime bookingTime) {
        this.bookingTime = bookingTime;
    }
}