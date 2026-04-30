const BASE_URL = "http://localhost:8080/api";
const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

if (!token) {
  window.location.href = "index.html";
}

let allBookings = [];
let currentFilter = "ALL";

let selectedEventId = null;
let selectedEventPrice = 0;
// Hide create button for CUSTOMER
window.onload = () => {
  if (role !== "ORGANIZER") {
    const createBtn = document.querySelector(".btn-primary");
    if (createBtn) createBtn.style.display = "none";
  }
};

// Logout
function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  window.location.href = "index.html";
}

// Load events
async function loadEvents() {
  const res = await fetch(`${BASE_URL}/events`, {
    headers: { Authorization: "Bearer " + token },
  });

  const events = await res.json();

  events.sort((a, b) => new Date(a.eventDate) - new Date(b.eventDate));
  window.allEvents = events;

  const container = document.getElementById("events");
  container.innerHTML = "";

  // Load carousel first
  loadCarousel(events);

  events.forEach((e) => {
    container.innerHTML += `
  <div class="event-card" onclick="openDetails(${e.id})">
    
    <!-- IMAGE -->
    <img 
      src="${e.imageUrl || "https://images.unsplash.com/photo-1507874457470-272b3c8d8ee2"}" 
      class="event-img"
    />

    <!-- CONTENT -->
    <div class="event-content">
      <h3>${e.name}</h3>
      <p>${e.description || "No description available"}</p>
     <p>${e.venue}</p>
<p class="event-date">${formatDate(e.eventDate)}</p>
      <p>₹${e.price}</p>
      <p>Seats: ${e.availableSeats}</p>

      <div class="card-actions">
        ${
          role === "CUSTOMER"
            ? `<button class="book-btn" onclick="event.stopPropagation(); openPayment(${e.id})">Book</button>`
            : `
             <button class="delete-btn" onclick="event.stopPropagation(); deleteEvent(${e.id})">
                Delete
              </button>
            `
        }
      </div>
    </div>

  </div>
`;
  });

  const statEvents = document.getElementById("stat-events");
  if (statEvents) statEvents.innerText = events.length;
}

// Book event
async function bookEvent(eventId) {
  const res = await fetch(`${BASE_URL}/bookings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + token,
    },
    body: JSON.stringify({
      eventId: eventId,
      numberOfTickets: 1,
    }),
  });

  if (res.ok) {
    alert("Booked successfully");
    await loadBookings();
    await loadEvents();
  } else {
    const msg = await res.text();
    alert("Booking failed: " + msg);
  }
}

// Load bookings
async function loadBookings() {
  const res = await fetch(`${BASE_URL}/bookings`, {
    headers: { Authorization: "Bearer " + token },
  });

  allBookings = await res.json();

  allBookings.sort((a, b) => b.id - a.id);

  updateStats();
  renderBookings();
}
//delete event
async function deleteEvent(id) {
  if (!confirm("Delete this event?")) return;

  const res = await fetch(`${BASE_URL}/events/${id}`, {
    method: "DELETE",
    headers: {
      Authorization: "Bearer " + token,
    },
  });

  if (res.ok) {
    alert("Event deleted");
    loadEvents();
  } else {
    const msg = await res.text();
    alert("Delete failed: " + msg);
  }
}
// Render bookings
function renderBookings() {
  const container = document.getElementById("bookings");
  container.innerHTML = "";

  let filtered = allBookings;

  if (currentFilter === "CONFIRMED") {
    filtered = allBookings.filter((b) => b.status === "CONFIRMED");
  } else if (currentFilter === "CANCELLED") {
    filtered = allBookings.filter((b) => b.status === "CANCELLED");
  }

  if (!filtered || filtered.length === 0) {
    container.innerHTML = "<p>No bookings</p>";
    return;
  }

  filtered.forEach((b) => {
    container.innerHTML += `
      <div class="card">
        <h3>${b.eventName}</h3>
        <p>Tickets: ${b.numberOfTickets}</p>
        <p>Status: ${b.status}</p>

        ${
          b.status === "CONFIRMED"
            ? `<button onclick="cancelBooking(${b.id})">Cancel</button>`
            : ""
        }
      </div>
    `;
  });
}

// Cancel booking
async function cancelBooking(id) {
  const booking = allBookings.find((b) => b.id === id);

  if (!booking) {
    alert("Booking not found");
    return;
  }

  const event = window.allEvents.find((e) => e.name === booking.eventName);

  if (!event) {
    alert("Event not found");
    return;
  }

  const eventTime = new Date(event.eventDate);
  const now = new Date();

  const diffHours = (eventTime - now) / (1000 * 60 * 60);

  if (diffHours < 3) {
    alert("Cannot cancel within 3 hours of the event");
    return;
  }

  const res = await fetch(`${BASE_URL}/bookings/${id}/cancel`, {
    method: "PUT",
    headers: { Authorization: "Bearer " + token },
  });

  if (res.ok) {
    alert("Cancelled");
    await loadBookings();
    await loadEvents();
  } else {
    const msg = await res.text();
    alert("Cancel failed: " + msg);
  }
}
// Filters
function showAll() {
  currentFilter = "ALL";
  renderBookings();
}

function showActive() {
  currentFilter = "CONFIRMED";
  renderBookings();
}

function showCancelled() {
  currentFilter = "CANCELLED";
  renderBookings();
}

// Stats
function updateStats() {
  const statBookings = document.getElementById("stat-bookings");
  const statConfirmed = document.getElementById("stat-confirmed");
  const statCancelled = document.getElementById("stat-cancelled");

  if (statBookings) statBookings.innerText = allBookings.length;

  const confirmed = allBookings.filter((b) => b.status === "CONFIRMED").length;
  const cancelled = allBookings.filter((b) => b.status === "CANCELLED").length;

  if (statConfirmed) statConfirmed.innerText = confirmed;
  if (statCancelled) statCancelled.innerText = cancelled;
}

// Navigation
function goToCreate() {
  window.location.href = "create-event.html";
}
function formatDate(dateStr) {
  const d = new Date(dateStr);

  return d.toLocaleString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function loadCarousel(events) {
  const container = document.getElementById("carousel");
  if (!container) return;

  const items = (events || []).slice(0, 5);

  if (items.length === 0) {
    container.innerHTML = "<p style='color:gray'>No events</p>";
    return;
  }

  let current = 0;

  function render() {
    const e = items[current];

    container.innerHTML = `
      <div class="hero-card">

        <!-- IMAGE -->
        <img 
          src="${e.imageUrl || "https://images.unsplash.com/photo-1507874457470-272b3c8d8ee2"}"
          class="hero-bg"
          onerror="this.src='https://images.unsplash.com/photo-1507874457470-272b3c8d8ee2'"
        />

        <!-- DARK OVERLAY -->
        <div class="hero-overlay"></div>

        <!-- CONTENT CARD -->
        <div class="hero-content">
          <h2>${e.name}</h2>
          <p>${e.description || "No description available"}</p>
          <p>${e.venue}</p>
          <p>₹${e.price} • Seats: ${e.availableSeats}</p>

          ${
            role === "CUSTOMER"
              ? `<button class="book-btn" onclick="openPayment(${e.id})">Book Now</button>`
              : `<span class="hero-tag">Organizer View</span>`
          }
        </div>

        <!-- NAV -->
        <button class="hero-nav left" onclick="prevSlide()">‹</button>
        <button class="hero-nav right" onclick="nextSlide()">›</button>

      </div>
    `;
  }

  window.nextSlide = function () {
    current = (current + 1) % items.length;
    render();
  };

  window.prevSlide = function () {
    current = (current - 1 + items.length) % items.length;
    render();
  };

  setInterval(() => {
    current = (current + 1) % items.length;
    render();
  }, 4000);

  render();
}
function openPayment(eventId) {
  selectedEventId = eventId;

  const event = window.allEvents.find((e) => e.id === eventId);
  selectedEventPrice = event.price;
  document.getElementById("paymentModal").classList.remove("hidden");

  document.getElementById("ticketCount").value = 1;
  updateTotal();

  document.getElementById("paymentModal").style.display = "block";
}

function updateTotal() {
  const tickets = parseInt(document.getElementById("ticketCount").value);

  const event = window.allEvents?.find((e) => e.id === selectedEventId);

  if (!event) return;

  const total = event.price * tickets;

  document.getElementById("totalAmount").innerText = "Total: ₹" + total;
}
function closePayment() {
  const modal = document.getElementById("paymentModal");

  modal.classList.add("hidden");
  modal.style.display = "none";
  // reset form
  document.getElementById("ticketCount").value = 1;
  document.getElementById("cardNumber").value = "";
  document.getElementById("cardName").value = "";
  document.getElementById("expiry").value = "";
  document.getElementById("cvv").value = "";
  document.getElementById("totalAmount").innerText = "Total: ₹0";
  document.body.style.overflow = "auto";
  selectedEventId = null;
}
async function processPayment() {
  const card = document.getElementById("cardNumber").value.trim();
  const name = document.getElementById("cardName").value.trim();
  const expiry = document.getElementById("expiry").value.trim();
  const cvv = document.getElementById("cvv").value.trim();
  const tickets = parseInt(document.getElementById("ticketCount").value);

  if (!card || !name || !expiry || !cvv || tickets < 1) {
    alert("Please fill all payment details correctly");
    return;
  }

  try {
    const loader = document.getElementById("loader");
    if (loader) loader.classList.remove("hidden");

    const res = await fetch(`${BASE_URL}/bookings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        eventId: selectedEventId,
        numberOfTickets: tickets,
      }),
    });

    if (!res.ok) {
      const msg = await res.text();
      alert("Booking failed: " + msg);
      return;
    }

    // SUCCESS
    alert("Payment Successful & Ticket Booked");

    // CLOSE MODAL PROPERLY
    const modal = document.getElementById("paymentModal");
    if (modal) modal.classList.add("hidden");

    document.body.style.overflow = "auto";
    selectedEventId = null;

    // RESET FORM
    document.getElementById("ticketCount").value = 1;
    document.getElementById("cardNumber").value = "";
    document.getElementById("cardName").value = "";
    document.getElementById("expiry").value = "";
    document.getElementById("cvv").value = "";
    document.getElementById("totalAmount").innerText = "Total: ₹0";

    // REFRESH DATA
    await loadBookings();
    await loadEvents();

    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (err) {
    console.error(err);
    alert("Payment error");
  } finally {
    const loader = document.getElementById("loader");
    if (loader) loader.classList.add("hidden");
  }
}
function filterEvents() {
  const search = document.getElementById("searchInput").value.toLowerCase();
  const venue = document.getElementById("venueFilter").value.toLowerCase();

  const filtered = window.allEvents.filter((e) => {
    const nameMatch = e.name.toLowerCase().includes(search);
    const venueMatch = e.venue.toLowerCase().includes(venue);

    return nameMatch && venueMatch;
  });

  renderFilteredEvents(filtered);
}
function renderFilteredEvents(events) {
  const container = document.getElementById("events");
  container.innerHTML = "";

  events.forEach((e) => {
    container.innerHTML += `
      <div class="event-card" onclick="openDetails(${e.id})">
        <img 
          src="${e.imageUrl || "https://images.unsplash.com/photo-1507874457470-272b3c8d8ee2"}" 
          class="event-img"
        />

        <div class="event-content">
          <h3>${e.name}</h3>
          <p>${e.description || "No description available"}</p>
         <p>${e.venue}</p>
<p class="event-date">${formatDate(e.eventDate)}</p>
          <p>₹${e.price}</p>
          <p>Seats: ${e.availableSeats}</p>

          <div class="card-actions">
            ${
              role === "CUSTOMER"
                ? `<button class="book-btn" onclick="openPayment(${e.id})">Book</button>`
                : `<button class="delete-btn" onclick="deleteEvent(${e.id})">Delete</button>`
            }
          </div>
        </div>
      </div>
    `;
  });
}
async function loadOrganizerBookings() {
  const res = await fetch(`${BASE_URL}/bookings/organizer`, {
    headers: { Authorization: "Bearer " + token },
  });

  if (!res.ok) {
    alert("Failed to load organizer bookings");
    return;
  }

  const data = await res.json();

  const container = document.getElementById("bookings");
  container.innerHTML = "";

  if (data.length === 0) {
    container.innerHTML = "<p>No bookings for your events</p>";
    return;
  }

  data.forEach((b) => {
    container.innerHTML += `
      <div class="card">
        <h3>${b.eventName}</h3>
        <p>User: ${b.userEmail}</p>
        <p>Tickets: ${b.numberOfTickets}</p>
        <p>Status: ${b.status}</p>
      </div>
    `;
  });
}
function openDetails(id) {
  const event = window.allEvents.find((e) => e.id === id);

  localStorage.setItem("selectedEvent", JSON.stringify(event));

  window.location.href = "event-details.html";
}
window.addEventListener("load", () => {
  const event = JSON.parse(localStorage.getItem("paymentEvent"));
  const tickets = localStorage.getItem("paymentTickets");

  if (event && tickets) {
    selectedEventId = event.id;
    selectedEventPrice = event.price;

    document.getElementById("paymentModal").classList.remove("hidden");
    document.getElementById("paymentModal").style.display = "flex";

    document.getElementById("ticketCount").value = tickets;
    updateTotal();

    localStorage.removeItem("paymentEvent");
    localStorage.removeItem("paymentTickets");
  }
});
// Init
if (role === "ORGANIZER") {
  loadEvents();
  loadOrganizerBookings();
} else {
  loadEvents();
  loadBookings();
}
