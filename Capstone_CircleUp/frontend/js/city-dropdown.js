/**
 * CircleUp — Custom City Dropdown
 * Searchable, keyboard-navigable city picker for major Indian cities.
 * Users can also type any custom location not in the list.
 */

const INDIAN_CITIES = [
  "Agra",
  "Ahmedabad",
  "Amritsar",
  "Aurangabad",
  "Bengaluru",
  "Bhopal",
  "Bhubaneswar",
  "Chandigarh",
  "Chennai",
  "Coimbatore",
  "Dehradun",
  "Delhi",
  "Faridabad",
  "Ghaziabad",
  "Gurugram",
  "Guwahati",
  "Gwalior",
  "Howrah",
  "Hubballi",
  "Hyderabad",
  "Indore",
  "Jabalpur",
  "Jaipur",
  "Jammu",
  "Jodhpur",
  "Kanpur",
  "Kochi",
  "Kolkata",
  "Kota",
  "Lucknow",
  "Ludhiana",
  "Madurai",
  "Mangaluru",
  "Meerut",
  "Mumbai",
  "Mysuru",
  "Nagpur",
  "Nashik",
  "Navi Mumbai",
  "Noida",
  "Patna",
  "Prayagraj",
  "Pune",
  "Raipur",
  "Rajkot",
  "Ranchi",
  "Shimla",
  "Siliguri",
  "Solapur",
  "Srinagar",
  "Thane",
  "Thiruvananthapuram",
  "Vadodara",
  "Varanasi",
  "Vijayawada",
  "Visakhapatnam",
];

/**
 * Initialize a searchable city dropdown.
 *
 * Required HTML structure:
 *   <div class="city-dropdown" id="<wrapperId>">
 *     <div class="city-input-wrap">
 *       <span class="city-search-icon">🔍</span>
 *       <input id="<inputId>" type="text" class="form-control city-input" autocomplete="off">
 *       <span class="city-arrow">
 *         <svg .../>
 *       </span>
 *     </div>
 *     <div class="city-list" id="<listId>"></div>
 *   </div>
 */
function initCityDropdown(inputId, listId, options = {}) {
  const input = document.getElementById(inputId);
  const list = document.getElementById(listId);
  if (!input || !list) return;

  const cities = options.cities || INDIAN_CITIES;
  const wrapper = list.closest(".city-dropdown");

  let isOpen = false;
  let highlighted = -1;
  let filtered = [...cities];

  // ── HTML escape ─────────────────────────────
  function h(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  // ── Highlight matched substring ──────────────
  function hlMatch(text, query) {
    if (!query) return h(text);
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return h(text);
    return (
      h(text.slice(0, idx)) +
      `<mark>${h(text.slice(idx, idx + query.length))}</mark>` +
      h(text.slice(idx + query.length))
    );
  }

  // ── Render list items ────────────────────────
  function render() {
    const q = input.value.trim();
    filtered = q
      ? cities.filter((c) => c.toLowerCase().includes(q.toLowerCase()))
      : [...cities];

    if (!filtered.length) {
      list.innerHTML = `
        <div class="city-no-results">
          <span class="city-nores-icon">🏙️</span>
          <div>
            <div class="city-nores-title">No matching city found</div>
            <div class="city-nores-sub">
              "<strong>${h(q)}</strong>" will be used as your custom location.
            </div>
          </div>
        </div>`;
      highlighted = -1;
      return;
    }

    const isAll = filtered.length === cities.length;
    const header = `<div class="city-list-header">
      <span>${isAll ? "🗺️ Popular cities in India" : `🔍 ${filtered.length} result${filtered.length !== 1 ? "s" : ""}`}</span>
    </div>`;

    list.innerHTML =
      header +
      filtered
        .map(
          (city, i) => `
      <div class="city-option ${i === highlighted ? "highlighted" : ""}"
           data-city="${h(city)}" data-idx="${i}">
        <span class="city-option-dot"></span>
        <span class="city-option-name">${hlMatch(city, q)}</span>
        ${i === highlighted ? '<span class="city-option-enter">↵</span>' : ""}
      </div>`,
        )
        .join("");

    list.querySelectorAll(".city-option").forEach((opt) => {
      opt.addEventListener("mousedown", (e) => {
        e.preventDefault();
        selectCity(opt.dataset.city);
      });
      opt.addEventListener("mouseenter", () => {
        highlighted = parseInt(opt.dataset.idx, 10);
        updateHL();
      });
    });
  }

  function updateHL() {
    list.querySelectorAll(".city-option").forEach((opt, i) => {
      const active = i === highlighted;
      opt.classList.toggle("highlighted", active);
      // update enter hint
      const existing = opt.querySelector(".city-option-enter");
      if (active && !existing)
        opt.insertAdjacentHTML(
          "beforeend",
          '<span class="city-option-enter">↵</span>',
        );
      if (!active && existing) existing.remove();
    });
    const el = list.querySelector(".city-option.highlighted");
    if (el) el.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  // ── Open / Close ─────────────────────────────
  function openDD() {
    if (isOpen) return;
    isOpen = true;
    highlighted = -1;
    render();
    list.classList.add("open");
    if (wrapper) wrapper.classList.add("open");
  }

  function closeDD() {
    if (!isOpen) return;
    isOpen = false;
    list.classList.remove("open");
    if (wrapper) wrapper.classList.remove("open");
    highlighted = -1;
  }

  function selectCity(city) {
    input.value = city;
    closeDD();
    input.classList.remove("input-invalid");
    input.classList.add("input-valid");
    const err = document.getElementById(inputId + "-error");
    if (err) err.textContent = "";
    input.dispatchEvent(new Event("change", { bubbles: true }));
    input.dispatchEvent(new Event("input", { bubbles: true }));
  }

  // ── Keyboard navigation ──────────────────────
  input.addEventListener("keydown", (e) => {
    if (!isOpen) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        openDD();
      }
      return;
    }
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        highlighted = Math.min(highlighted + 1, filtered.length - 1);
        updateHL();
        break;
      case "ArrowUp":
        e.preventDefault();
        highlighted = Math.max(highlighted - 1, -1);
        updateHL();
        break;
      case "Enter":
        e.preventDefault();
        if (highlighted >= 0 && filtered[highlighted])
          selectCity(filtered[highlighted]);
        else closeDD();
        break;
      case "Escape":
        closeDD();
        break;
    }
  });

  input.addEventListener("focus", openDD);
  input.addEventListener("input", () => {
    highlighted = -1;
    if (!isOpen) openDD();
    else render();
  });
  input.addEventListener("blur", () => setTimeout(closeDD, 180));
  document.addEventListener("click", (e) => {
    if (wrapper && !wrapper.contains(e.target)) closeDD();
  });
}
