const BASE_URL = "http://localhost:8080/api";
const token = localStorage.getItem("token");

// Loader
function showLoader() {
  document.getElementById("loader").classList.remove("hidden");
}

function hideLoader() {
  document.getElementById("loader").classList.add("hidden");
}

// Toast
function showToast(msg) {
  const toast = document.getElementById("toast");
  toast.innerText = msg;
  toast.classList.add("show");

  setTimeout(() => toast.classList.remove("show"), 3000);
}

// CREATE EVENT
async function createNewEvent() {
  showLoader();

  const data = {
    name: document.getElementById("name").value,
    description: document.getElementById("description").value,
    venue: document.getElementById("venue").value,
    eventDate: document.getElementById("eventDate").value,
    price: Number(document.getElementById("price").value),
    totalSeats: Number(document.getElementById("totalSeats").value),
    imageUrl: document.getElementById("imageUrl").value.trim(),
  };

  try {
    const response = await fetch(`${BASE_URL}/events`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify(data),
    });

    hideLoader();

    if (response.ok) {
      showToast("Event Created");

      // redirect after success
      setTimeout(() => {
        window.location.href = "dashboard.html";
      }, 800);
    } else {
      const msg = await response.text();
      showToast("Error: " + msg);
    }
  } catch (e) {
    hideLoader();
    console.error(e);
    showToast("Server error");
  }
}

// Back button
function goBack() {
  window.location.href = "dashboard.html";
}
