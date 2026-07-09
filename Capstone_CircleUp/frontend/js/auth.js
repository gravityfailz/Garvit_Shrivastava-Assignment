/* ---- Token storage ---- */
const TOKEN_KEY = "circleup_token";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}
function setToken(t) {
  localStorage.setItem(TOKEN_KEY, t);
}
function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}
function isLoggedIn() {
  return !!getToken();
}

function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = "./login.html";
    return false;
  }
  return true;
}

function redirectIfLoggedIn() {
  if (isLoggedIn()) window.location.href = "./activities.html";
}

/* ---- Initials helper ---- */
function getInitials(name) {
  if (!name) return "?";
  return name
    .trim()
    .split(/\s+/)
    .map((p) => p[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
}

/* ---- Navbar user info ---- */
function renderNavUser(name) {
  const initialsEl = document.getElementById("nav-initials");
  const nameEl = document.getElementById("nav-user-name");
  if (initialsEl) initialsEl.textContent = getInitials(name);
  if (nameEl) nameEl.textContent = name;
}

/* ---- Logout ---- */
async function logout() {
  try {
    await apiRequest("/auth/logout", { method: "POST" });
  } catch (_) {}
  clearToken();
  window.location.href = "./login.html";
}
