const BASE_URL = "http://localhost:8080/api";
const token = localStorage.getItem("token");

if (!token) {
  window.location.href = "index.html";
}

let allBookings = [];
let currentFilter = "ALL";

// Logout
function logout() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

// ---------------- EVENTS ----------------
async function loadEvents() {
  const res = await fetch(`${BASE_URL}/events`, {
    headers: { Authorization: "Bearer " + token },
  });

  const events = await res.json();

  const container = document.getElementById("events");
  container.innerHTML = "";

  events.forEach((e) => {
    container.innerHTML += `
      <div class="card">
        <h3>${e.name}</h3>
        <p>${e.description || "No description"}</p>
        <p>${e.venue}</p>
        <p>₹${e.price}</p>
        <p>Seats: ${e.availableSeats}</p>
        <button onclick="bookEvent(${e.id})">Book</button>
      </div>
    `;
  });

  document.getElementById("stat-events").innerText = events.length;
}

// ---------------- BOOK EVENT ----------------
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

    await loadBookings(); // refresh bookings
    await loadEvents(); // refresh events (important)
  } else {
    alert("Booking failed");
  }
}

// ---------------- LOAD BOOKINGS ----------------
async function loadBookings() {
  const res = await fetch(`${BASE_URL}/bookings`, {
    headers: { Authorization: "Bearer " + token },
  });

  allBookings = await res.json();

  updateStats();
  renderBookings();
}

// ---------------- RENDER BOOKINGS ----------------
function renderBookings() {
  const container = document.getElementById("bookings");
  container.innerHTML = "";

  let filtered = allBookings;

  if (currentFilter === "CONFIRMED") {
    filtered = allBookings.filter((b) => b.status === "CONFIRMED");
  } else if (currentFilter === "CANCELLED") {
    filtered = allBookings.filter((b) => b.status === "CANCELLED");
  }

  if (filtered.length === 0) {
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

// ---------------- CANCEL BOOKING ----------------
async function cancelBooking(id) {
  const res = await fetch(`${BASE_URL}/bookings/${id}/cancel`, {
    method: "PUT", //
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

// ---------------- FILTERS ----------------
function showAll() {
  currentFilter = "ALL";
  renderBookings();
}

function showActive() {
  currentFilter = "CONFIRMED"; // ✅ FIXED
  renderBookings();
}

function showCancelled() {
  currentFilter = "CANCELLED";
  renderBookings();
}

// ---------------- STATS ----------------
function updateStats() {
  document.getElementById("stat-bookings").innerText = allBookings.length;

  const confirmed = allBookings.filter((b) => b.status === "CONFIRMED").length;
  const cancelled = allBookings.filter((b) => b.status === "CANCELLED").length;

  document.getElementById("stat-confirmed").innerText = confirmed;
  document.getElementById("stat-cancelled").innerText = cancelled;
}

// ---------------- NAV ----------------
function goToCreate() {
  window.location.href = "create-event.html";
}

// ---------------- INIT ----------------
loadEvents();
loadBookings();
