/* ---- Core fetch wrapper ---- */
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

  // Token invalid/expired — wipe it and redirect
  if (
    response.status === 401 &&
    window.location.pathname !== "/login.html" &&
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

/* ---- UI helpers ---- */
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
  const d = new Date();
  d.setHours(+h, +m);
  return d.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" });
}

function statusBadge(s) {
  return `<span class="badge badge-${s}">${s}</span>`;
}

function esc(str) {
  const d = document.createElement("div");
  d.appendChild(document.createTextNode(str));
  return d.innerHTML;
}
