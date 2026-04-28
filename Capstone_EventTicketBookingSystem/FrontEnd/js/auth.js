const BASE_URL = "http://localhost:8080/api";

// LOGIN
async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch(
      `${BASE_URL}/auth/login?email=${email}&password=${password}`,
      { method: "POST" },
    );

    // CHECK IF FAILED
    if (!response.ok) {
      const errorText = await response.text();
      alert("Login failed: " + errorText);
      return;
    }

    const token = await response.text();

    // CHECK EMPTY TOKEN
    if (!token || token.length < 10) {
      alert("Invalid login response");
      return;
    }

    localStorage.setItem("token", token);

    alert("Login Successful 🎉");

    window.location.href = "dashboard.html";
  } catch (error) {
    console.error(error);
    alert("Server error. Check backend.");
  }
}

// REGISTER
async function register() {
  const data = {
    name: document.getElementById("name").value.trim(),
    email: document.getElementById("email").value.trim(),
    password: document.getElementById("password").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    role: "CUSTOMER",
  };

  try {
    const response = await fetch(`${BASE_URL}/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.text();

    console.log("Response:", result);

    if (!response.ok) {
      alert("Registration failed: " + result);
      return;
    }

    alert("Registered successfully 🎉");
    window.location.href = "index.html";
  } catch (error) {
    console.error("ERROR:", error);
    alert("Server not reachable / backend issue");
  }
}

// LOAD EVENTS
async function loadEvents() {
  const token = localStorage.getItem("token");

  const res = await fetch(`${BASE_URL}/events`, {
    headers: {
      Authorization: "Bearer " + token,
    },
  });

  const events = await res.json();

  const container = document.getElementById("events");
  container.innerHTML = "";

  events.forEach((e) => {
    container.innerHTML += `
            <div class="card">
                <h3>${e.name}</h3>
                <p>${e.venue}</p>
                <p>₹${e.price}</p>
            </div>
        `;
  });
}
let selectedEventId = null;

// LOAD EVENTS (UPDATED UI)
async function loadEvents() {
  const token = localStorage.getItem("token");

  const res = await fetch(`${BASE_URL}/events`, {
    headers: {
      Authorization: "Bearer " + token,
    },
  });

  const events = await res.json();

  const container = document.getElementById("events");
  container.innerHTML = "";

  events.forEach((e) => {
    container.innerHTML += `
            <div class="card">
                <h3>${e.name}</h3>
                <p>📍 ${e.venue}</p>
                <p>💰 ₹${e.price}</p>
                <p>🎫 Seats: ${e.availableSeats}</p>
                <button class="book-btn" onclick="openModal(${e.id})">
                    Book Now
                </button>
            </div>
        `;
  });
}

// OPEN MODAL
function openModal(eventId) {
  selectedEventId = eventId;
  document.getElementById("modal").style.display = "block";
}

// CLOSE MODAL
function closeModal() {
  document.getElementById("modal").style.display = "none";
}

// CONFIRM BOOKING
async function confirmBooking() {
  const tickets = document.getElementById("tickets").value;
  const token = localStorage.getItem("token");

  await fetch(`${BASE_URL}/bookings`, {
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

  alert("Booking Successful 🎉");
  closeModal();
  loadEvents();
}
