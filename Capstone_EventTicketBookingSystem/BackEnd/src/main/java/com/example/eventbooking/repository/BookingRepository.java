package com.example.eventbooking.repository;

import com.example.eventbooking.entity.Booking;
import com.example.eventbooking.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface BookingRepository extends JpaRepository<Booking, Long> {

    List<Booking> findByUser(User user);

    void deleteByEventId(Long eventId);

    List<Booking> findByEventOrganizerEmail(String email);

}