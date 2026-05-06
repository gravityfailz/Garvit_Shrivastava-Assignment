package com.example.eventbooking.controller;

import com.example.eventbooking.service.EventService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.List;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@ExtendWith(MockitoExtension.class)
public class EventControllerTest {

    @Mock
    private EventService eventService;

    @InjectMocks
    private EventController eventController;

    private MockMvc mockMvc() {
        return MockMvcBuilders.standaloneSetup(eventController).build();
    }

    @Test
    void testGetAllEvents() throws Exception {
        when(eventService.getAllEvents()).thenReturn(List.of());
        mockMvc().perform(get("/api/events"))
                .andExpect(status().isOk());
    }

    @Test
    void testGetEventById() throws Exception {
        when(eventService.getEventById(1L)).thenReturn(null);
        mockMvc().perform(get("/api/events/1"))
                .andExpect(status().isOk());
    }

    @Test
    void testGetAllEventsAgain() throws Exception {
        when(eventService.getAllEvents()).thenReturn(List.of());
        mockMvc().perform(get("/api/events"))
                .andExpect(status().isOk());
    }

    @Test
    void testGetUpcomingEvents() throws Exception {
        when(eventService.getUpcomingEvents()).thenReturn(List.of());
        mockMvc().perform(get("/api/events/upcoming"))
                .andExpect(status().isOk());
    }

    @Test
    void testGetPastEvents() throws Exception {
        when(eventService.getPastEvents()).thenReturn(List.of());
        mockMvc().perform(get("/api/events/past"))
                .andExpect(status().isOk());
    }

    @Test
    void testGetCancelledEvents() throws Exception {
        when(eventService.getCancelledEvents()).thenReturn(List.of());
        mockMvc().perform(get("/api/events/cancelled"))
                .andExpect(status().isOk());
    }
}