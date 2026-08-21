async function apiRequest(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  } catch (_) {
    throw { status: 0, detail: "Network error. Is the backend running?" };
  }

  if (
    response.status === 401 &&
    !window.location.pathname.endsWith("login.html") &&
    !endpoint.includes("/auth/")
  ) {
    clearToken();
    window.location.href = "./login.html";
    return;
  }

  let data;
  try {
    data = await response.json();
  } catch (_) {
    data = {};
  }
  if (!response.ok)
    throw {
      status: response.status,
      detail: data.detail || "Something went wrong.",
    };
  return data;
}

/* ---- Alert helpers ---- */
function showAlert(id, msg, type = "error") {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = msg;
  el.className = `alert alert-${type} show`;
}
function hideAlert(id) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = "";
    el.className = "alert";
  }
}
function setLoading(btn, on, label) {
  if (on) {
    btn.disabled = true;
    btn.dataset.orig = btn.textContent;
    btn.textContent = label || "Loading…";
  } else {
    btn.disabled = false;
    btn.textContent = btn.dataset.orig || "Submit";
  }
}

/* ---- Toast notifications ---- */
function showToast(message, type = "error", duration = 5000, title = null) {
  let container = document.getElementById("cu-toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "cu-toast-container";
    container.className = "cu-toast-container";
    document.body.appendChild(container);
  }

  const icons = { error: "⛔", success: "✅", warning: "⚠️", info: "ℹ️" };
  const labels = {
    error: "Error",
    success: "Success",
    warning: "Heads up!",
    info: "Info",
  };

  const toast = document.createElement("div");
  toast.className = `cu-toast cu-toast-${type}`;
  toast.innerHTML = `
    <div class="cu-toast-left">
      <span class="cu-toast-icon">${icons[type] || "📢"}</span>
    </div>
    <div class="cu-toast-body">
      <div class="cu-toast-title">${esc(title || labels[type] || "")}</div>
      <div class="cu-toast-msg">${message}</div>
    </div>
    <button class="cu-toast-close" onclick="this.closest('.cu-toast').remove()" title="Dismiss">✕</button>
  `;

  container.appendChild(toast);
  // Force reflow so the CSS animation triggers
  toast.getBoundingClientRect();
  toast.classList.add("cu-toast-in");

  if (duration > 0) {
    setTimeout(() => {
      toast.classList.add("cu-toast-out");
      setTimeout(() => toast.remove(), 380);
    }, duration);
  }
}

/* ---- Formatting ---- */
function fmtDate(d) {
  if (!d) return "";
  const [y, m, day] = d.split("-");
  return new Date(+y, +m - 1, +day).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function fmtTime(t) {
  if (!t) return "";
  const [h, m] = t.split(":");
  const dt = new Date();
  dt.setHours(+h, +m);
  return dt.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" });
}

function statusBadge(s) {
  return `<span class="badge badge-${s}">${s}</span>`;
}

function esc(str) {
  const d = document.createElement("div");
  d.appendChild(document.createTextNode(str));
  return d.innerHTML;
}
