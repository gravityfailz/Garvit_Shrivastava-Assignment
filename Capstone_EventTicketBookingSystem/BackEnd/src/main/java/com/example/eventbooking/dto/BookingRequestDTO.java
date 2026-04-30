package com.example.eventbooking.dto;

import jakarta.validation.constraints.*;

public class BookingRequestDTO {

    @NotNull
    private Long eventId;

    @Min(1)
    private int numberOfTickets;

    // getters & setters
    public Long getEventId() {
        return eventId;
    }

    public void setEventId(Long eventId) {
        this.eventId = eventId;
    }

    public int getNumberOfTickets() {
        return numberOfTickets;
    }

    public void setNumberOfTickets(int numberOfTickets) {
        this.numberOfTickets = numberOfTickets;
    }
}