/**
 * CircleUp — Validation utilities (Week 3 final, phone 6-10 digits)
 */

const Validators = {
  email(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value).trim());
  },

  password(value) {
    const v = String(value);
    return {
      minLength: v.length >= 8,
      hasUppercase: /[A-Z]/.test(v),
      hasNumber: /\d/.test(v),
      get isValid() {
        return this.minLength && this.hasUppercase && this.hasNumber;
      },
    };
  },

  /** Phone: 6–10 digits only */
  phone(value) {
    const digits = String(value).replace(/\D/g, "");
    return digits.length >= 6 && digits.length <= 10;
  },

  required(value) {
    return value != null && String(value).trim().length > 0;
  },
};

/** Returns true if the combined date + time is strictly in the future. */
function isFutureDatetime(dateStr, timeStr) {
  if (!dateStr || !timeStr) return false;
  const [h, m] = timeStr.split(":");
  const selected = new Date(dateStr);
  selected.setHours(parseInt(h, 10), parseInt(m, 10), 0, 0);
  return selected > new Date();
}

/** Update the password requirements checklist in real-time. */
function updatePasswordRequirements(password) {
  const checks = Validators.password(password);
  const map = {
    "req-length": checks.minLength,
    "req-uppercase": checks.hasUppercase,
    "req-number": checks.hasNumber,
  };
  Object.entries(map).forEach(([id, met]) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.className = `req-item ${met ? "req-met" : "req-unmet"}`;
    const icon = el.querySelector(".req-icon");
    if (icon) icon.textContent = met ? "✓" : "○";
  });
}

/** Mark an input valid / invalid and show / hide its error. */
function setFieldState(inputEl, valid, errorMsg) {
  if (!inputEl) return;
  inputEl.classList.remove("input-valid", "input-invalid");
  const err = document.getElementById(inputEl.id + "-error");
  if (valid === null) {
    if (err) err.textContent = "";
    return;
  }
  if (valid) {
    inputEl.classList.add("input-valid");
    if (err) err.textContent = "";
  } else {
    inputEl.classList.add("input-invalid");
    if (err) err.textContent = errorMsg || "This field is required.";
  }
}

/** Toggle password show / hide. */
function togglePasswordVisibility(inputId, btnEl) {
  const input = document.getElementById(inputId);
  if (!input) return;
  const hidden = input.type === "password";
  input.type = hidden ? "text" : "password";
  btnEl.textContent = hidden ? "🙈" : "👁";
}
