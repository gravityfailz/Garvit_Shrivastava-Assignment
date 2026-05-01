const event = JSON.parse(localStorage.getItem("selectedEvent"));

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

document.getElementById("eventImg").src =
  event.imageUrl ||
  "https://images.unsplash.com/photo-1507874457470-272b3c8d8ee2";

document.getElementById("eventName").innerText = event.name;
document.getElementById("eventVenue").innerText = event.venue;
document.getElementById("eventDate").innerText = formatDate(event.eventDate);
document.getElementById("eventPrice").innerText = "₹" + event.price;
document.getElementById("eventDesc").innerText =
  event.description || "No description available";

document.getElementById("venueText").innerText = event.venue;
document.getElementById("dateText").innerText = formatDate(event.eventDate);
document.getElementById("priceText").innerText = event.price;

let tickets = 1;

function updateTotal() {
  tickets = parseInt(document.getElementById("ticketCount").value);
  const total = tickets * event.price;
  document.getElementById("totalAmount").innerText = "Total: ₹" + total;
}

updateTotal();

function proceedToPayment() {
  if (!tickets || tickets < 1) {
    alert("Invalid ticket count");
    return;
  }

  localStorage.setItem("paymentEvent", JSON.stringify(event));
  localStorage.setItem("paymentTickets", tickets);

  window.location.href = "dashboard.html";
}

function goBack() {
  window.location.href = "dashboard.html";
}
