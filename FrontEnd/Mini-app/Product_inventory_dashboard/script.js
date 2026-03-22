const defaultProducts = [
  {
    id: 1,
    name: "Laptop Pro 15",
    price: 75000,
    stock: 12,
    category: "electronics",
  },
  {
    id: 2,
    name: "Wireless Headphones",
    price: 3500,
    stock: 25,
    category: "electronics",
  },
  {
    id: 3,
    name: "Cotton T-Shirt",
    price: 599,
    stock: 50,
    category: "clothing",
  },
  {
    id: 4,
    name: "JavaScript: The Good Parts",
    price: 450,
    stock: 8,
    category: "books",
  },
  {
    id: 5,
    name: "Leather Wallet",
    price: 1200,
    stock: 15,
    category: "accessories",
  },
  {
    id: 6,
    name: "Smart Watch X1",
    price: 12000,
    stock: 0,
    category: "electronics",
  },
  { id: 7, name: "Denim Jeans", price: 1499, stock: 30, category: "clothing" },
  { id: 8, name: "Clean Code", price: 550, stock: 3, category: "books" },
  {
    id: 9,
    name: "Sunglasses Premium",
    price: 2500,
    stock: 20,
    category: "accessories",
  },
  {
    id: 10,
    name: "Bluetooth Speaker",
    price: 4500,
    stock: 18,
    category: "electronics",
  },
  { id: 11, name: "Running Shoes", price: 3200, stock: 0, category: "sports" },
  { id: 12, name: "Yoga Mat", price: 800, stock: 45, category: "sports" },
  { id: 13, name: "Coffee Maker", price: 5500, stock: 7, category: "home" },
  {
    id: 14,
    name: "Throw Pillow Set",
    price: 1200,
    stock: 22,
    category: "home",
  },
  {
    id: 15,
    name: "Winter Jacket",
    price: 2999,
    stock: 4,
    category: "clothing",
  },
];

// 2. Application State Management

let appState = {
  products: [],
  filteredProducts: [],
  currentPage: 1,
  itemsPerPage: 8,
  searchQuery: "",
  categoryFilter: "all",
  stockFilter: "all",
  sortOption: "default",
};

// 3. DOM Element References

const elements = {
  // Loading and App containers
  loadingOverlay: document.getElementById("loading-overlay"),
  app: document.getElementById("app"),

  // Control elements
  searchInput: document.getElementById("search-input"),
  clearSearchBtn: document.getElementById("clear-search"),
  categoryFilter: document.getElementById("category-filter"),
  stockFilter: document.getElementById("stock-filter"),
  sortSelect: document.getElementById("sort-select"),

  // Product display elements
  productGrid: document.getElementById("product-grid"),
  emptyState: document.getElementById("empty-state"),
  productCount: document.getElementById("product-count"),

  // Analytics elements
  totalProducts: document.getElementById("total-products"),
  totalValue: document.getElementById("total-value"),
  outOfStock: document.getElementById("out-of-stock"),
  lowStock: document.getElementById("low-stock"),

  // Pagination elements
  pagination: document.getElementById("pagination"),
  prevPageBtn: document.getElementById("prev-page"),
  nextPageBtn: document.getElementById("next-page"),
  pageInfo: document.getElementById("page-info"),

  // Form elements
  addProductForm: document.getElementById("add-product-form"),
  productName: document.getElementById("product-name"),
  productPrice: document.getElementById("product-price"),
  productStock: document.getElementById("product-stock"),
  productCategory: document.getElementById("product-category"),

  // Error message elements
  nameError: document.getElementById("name-error"),
  priceError: document.getElementById("price-error"),
  stockError: document.getElementById("stock-error"),
  categoryError: document.getElementById("category-error"),

  // Modal elements
  editModal: document.getElementById("edit-modal"),
  closeModalBtn: document.getElementById("close-modal"),
  cancelEditBtn: document.getElementById("cancel-edit"),
  editProductForm: document.getElementById("edit-product-form"),
  editProductId: document.getElementById("edit-product-id"),
  editProductName: document.getElementById("edit-product-name"),
  editProductPrice: document.getElementById("edit-product-price"),
  editProductStock: document.getElementById("edit-product-stock"),
  editProductCategory: document.getElementById("edit-product-category"),

  // Toast container
  toastContainer: document.getElementById("toast-container"),
};

// 4. LocalStorage Functions

function saveToLocalStorage() {
  try {
    localStorage.setItem(
      "inventoryProducts",
      JSON.stringify(appState.products),
    );
  } catch (error) {
    console.error("Error saving to localStorage:", error);
    showToast("Failed to save data", "error");
  }
}

function loadFromLocalStorage() {
  try {
    const storedData = localStorage.getItem("inventoryProducts");
    if (storedData) {
      const parsedData = JSON.parse(storedData);
      // Validate that parsed data is an array
      if (Array.isArray(parsedData) && parsedData.length > 0) {
        return parsedData;
      }
    }
  } catch (error) {
    console.error("Error loading from localStorage:", error);
  }
  // Return default products if localStorage is empty or invalid
  return [...defaultProducts];
}

// 5. Simulated API Loading (Async)

function fetchProducts() {
  return new Promise((resolve) => {
    // Simulate network delay of 1.5 seconds
    setTimeout(() => {
      const products = loadFromLocalStorage();
      resolve(products);
    }, 1500);
  });
}

async function initializeApp() {
  try {
    // Show loading state
    elements.loadingOverlay.classList.remove("hidden");
    elements.app.classList.add("hidden");

    // Fetch products using simulated API
    const products = await fetchProducts();
    appState.products = products;

    // Initialize the UI
    populateCategoryFilter();
    applyFiltersAndSort();
    updateAnalytics();

    // Hide loading and show app
    elements.loadingOverlay.classList.add("hidden");
    elements.app.classList.remove("hidden");
  } catch (error) {
    console.error("Error initializing app:", error);
    showToast("Failed to load products", "error");

    // Still show app even if there's an error
    elements.loadingOverlay.classList.add("hidden");
    elements.app.classList.remove("hidden");
  }
}

// 6. Analytics Calculation Functions

function updateAnalytics() {
  const products = appState.products;

  // Calculate total number of products
  const totalProductCount = products.length;

  // Calculate total inventory value (price * stock for each product)
  const totalInventoryValue = products.reduce((sum, product) => {
    return sum + product.price * product.stock;
  }, 0);

  // Count products with zero stock
  const outOfStockCount = products.filter(
    (product) => product.stock === 0,
  ).length;

  // Count products with low stock (stock < 5 but not zero)
  const lowStockCount = products.filter(
    (product) => product.stock > 0 && product.stock < 5,
  ).length;

  // Update DOM elements with calculated values
  elements.totalProducts.textContent = totalProductCount;
  elements.totalValue.textContent = formatCurrency(totalInventoryValue);
  elements.outOfStock.textContent = outOfStockCount;
  elements.lowStock.textContent = lowStockCount;
}

function formatCurrency(amount) {
  return "₹" + amount.toLocaleString("en-IN");
}

// 7. Category Filter Population

function populateCategoryFilter() {
  // Get unique categories from products
  const categories = [
    ...new Set(appState.products.map((product) => product.category)),
  ];

  // Clear existing options except "All Categories"
  elements.categoryFilter.innerHTML =
    '<option value="all">All Categories</option>';

  // Add option for each unique category
  categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category;
    // Capitalize first letter for display
    option.textContent = category.charAt(0).toUpperCase() + category.slice(1);
    elements.categoryFilter.appendChild(option);
  });
}

// 8. Filtering and Sorting Functions

function applyFiltersAndSort() {
  let filtered = [...appState.products];

  // Apply search filter (case-insensitive name matching)
  if (appState.searchQuery) {
    const query = appState.searchQuery.toLowerCase().trim();
    filtered = filtered.filter((product) =>
      product.name.toLowerCase().includes(query),
    );
  }

  // Apply category filter
  if (appState.categoryFilter !== "all") {
    filtered = filtered.filter(
      (product) => product.category === appState.categoryFilter,
    );
  }

  // Apply stock filter
  if (appState.stockFilter !== "all") {
    switch (appState.stockFilter) {
      case "low":
        // Stock less than 5 but greater than 0
        filtered = filtered.filter(
          (product) => product.stock > 0 && product.stock < 5,
        );
        break;
      case "out":
        // Zero stock
        filtered = filtered.filter((product) => product.stock === 0);
        break;
      case "in":
        // Stock 5 or more
        filtered = filtered.filter((product) => product.stock >= 5);
        break;
    }
  }

  // Apply sorting
  filtered = sortProducts(filtered, appState.sortOption);

  // Update state with filtered results
  appState.filteredProducts = filtered;

  // Reset to first page when filters change
  appState.currentPage = 1;

  // Render the filtered products
  renderProducts();
  updatePagination();
}

function sortProducts(products, sortOption) {
  const sorted = [...products];

  switch (sortOption) {
    case "price-low":
      // Sort by price ascending (low to high)
      sorted.sort((a, b) => a.price - b.price);
      break;
    case "price-high":
      // Sort by price descending (high to low)
      sorted.sort((a, b) => b.price - a.price);
      break;
    case "name-az":
      // Sort alphabetically A to Z
      sorted.sort((a, b) => a.name.localeCompare(b.name));
      break;
    case "name-za":
      // Sort alphabetically Z to A
      sorted.sort((a, b) => b.name.localeCompare(a.name));
      break;
    default:
      // Default: sort by ID (original order)
      sorted.sort((a, b) => a.id - b.id);
  }

  return sorted;
}

// 9. Product Rendering Functions

function renderProducts() {
  const { filteredProducts, currentPage, itemsPerPage } = appState;

  // Calculate pagination bounds
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const productsToShow = filteredProducts.slice(startIndex, endIndex);

  // Update product count display
  elements.productCount.textContent = `Showing ${productsToShow.length} of ${filteredProducts.length} products`;

  // Handle empty state
  if (filteredProducts.length === 0) {
    elements.productGrid.innerHTML = "";
    elements.emptyState.classList.remove("hidden");
    elements.pagination.classList.add("hidden");
    return;
  }

  // Hide empty state and show products
  elements.emptyState.classList.add("hidden");

  // Clear existing cards and render new ones
  elements.productGrid.innerHTML = "";

  productsToShow.forEach((product, index) => {
    const card = createProductCard(product);
    // Add staggered animation delay for visual effect
    card.style.animationDelay = `${index * 0.05}s`;
    elements.productGrid.appendChild(card);
  });
}

function createProductCard(product) {
  const card = document.createElement("article");
  card.className = "product-card";
  card.dataset.productId = product.id;

  // Determine stock status and corresponding class
  let stockClass = "stock-in";
  let stockLabel = "In Stock";

  if (product.stock === 0) {
    stockClass = "stock-out";
    stockLabel = "Out of Stock";
  } else if (product.stock < 5) {
    stockClass = "stock-low";
    stockLabel = "Low Stock";
  }

  // Build card HTML structure
  card.innerHTML = `
        <div class="product-card-header">
            <h3 class="product-name">${escapeHTML(product.name)}</h3>
            <span class="category-badge category-${product.category}">
                ${product.category}
            </span>
        </div>
        <div class="product-card-body">
            <div class="product-detail">
                <span class="product-detail-label">Price</span>
                <span class="product-detail-value product-price">${formatCurrency(product.price)}</span>
            </div>
            <div class="product-detail">
                <span class="product-detail-label">Stock</span>
                <span class="stock-indicator ${stockClass}">
                    ${product.stock} units - ${stockLabel}
                </span>
            </div>
        </div>
        <div class="product-card-footer">
            <button class="btn btn-edit" onclick="openEditModal(${product.id})" title="Edit product">
                ✏️ Edit
            </button>
            <button class="btn btn-danger" onclick="deleteProduct(${product.id})" title="Delete product">
                🗑️ Delete
            </button>
        </div>
    `;

  return card;
}

function escapeHTML(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// 10. Pagination Functions

function updatePagination() {
  const { filteredProducts, currentPage, itemsPerPage } = appState;
  const totalPages = Math.ceil(filteredProducts.length / itemsPerPage);

  // Hide pagination if only one page or no products
  if (totalPages <= 1) {
    elements.pagination.classList.add("hidden");
    return;
  }

  // Show pagination
  elements.pagination.classList.remove("hidden");

  // Update page info text
  elements.pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

  // Update button states
  elements.prevPageBtn.disabled = currentPage === 1;
  elements.nextPageBtn.disabled = currentPage === totalPages;
}

function goToPreviousPage() {
  if (appState.currentPage > 1) {
    appState.currentPage--;
    renderProducts();
    updatePagination();
    scrollToProductSection();
  }
}

function goToNextPage() {
  const totalPages = Math.ceil(
    appState.filteredProducts.length / appState.itemsPerPage,
  );
  if (appState.currentPage < totalPages) {
    appState.currentPage++;
    renderProducts();
    updatePagination();
    scrollToProductSection();
  }
}

function scrollToProductSection() {
  document.querySelector(".products-section").scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

// 11. Product CRUD Operations

function generateProductId() {
  // Find the highest existing ID and add 1
  const maxId = appState.products.reduce(
    (max, product) => Math.max(max, product.id),
    0,
  );
  return maxId + 1;
}

function addProduct(event) {
  event.preventDefault();

  // Clear previous error messages
  clearFormErrors();

  // Get form values
  const name = elements.productName.value.trim();
  const price = parseFloat(elements.productPrice.value);
  const stock = parseInt(elements.productStock.value);
  const category = elements.productCategory.value;

  // Validate form data
  let isValid = true;

  if (!name) {
    showFieldError("name", "Product name is required");
    isValid = false;
  } else if (name.length < 2) {
    showFieldError("name", "Name must be at least 2 characters");
    isValid = false;
  }

  if (isNaN(price) || price <= 0) {
    showFieldError("price", "Price must be greater than 0");
    isValid = false;
  }

  if (isNaN(stock) || stock < 0) {
    showFieldError("stock", "Stock cannot be negative");
    isValid = false;
  }

  if (!category) {
    showFieldError("category", "Please select a category");
    isValid = false;
  }

  // Stop if validation failed
  if (!isValid) {
    return;
  }

  // Create new product object
  const newProduct = {
    id: generateProductId(),
    name: name,
    price: price,
    stock: stock,
    category: category,
  };

  // Add to products array
  appState.products.push(newProduct);

  // Save to localStorage
  saveToLocalStorage();

  // Update UI
  populateCategoryFilter();
  applyFiltersAndSort();
  updateAnalytics();

  // Reset form
  elements.addProductForm.reset();

  // Show success message
  showToast(`Product "${name}" added successfully!`, "success");
}

function deleteProduct(productId) {
  // Find the product to get its name for the message
  const product = appState.products.find((p) => p.id === productId);

  if (!product) {
    showToast("Product not found", "error");
    return;
  }

  // Confirm deletion
  if (!confirm(`Are you sure you want to delete "${product.name}"?`)) {
    return;
  }

  // Remove product from array
  appState.products = appState.products.filter((p) => p.id !== productId);

  // Save to localStorage
  saveToLocalStorage();

  // Update UI
  populateCategoryFilter();
  applyFiltersAndSort();
  updateAnalytics();

  // Show success message
  showToast(`Product "${product.name}" deleted`, "success");
}

// 12. Edit Product Modal Functions

function openEditModal(productId) {
  const product = appState.products.find((p) => p.id === productId);

  if (!product) {
    showToast("Product not found", "error");
    return;
  }

  // Fill form with current product data
  elements.editProductId.value = product.id;
  elements.editProductName.value = product.name;
  elements.editProductPrice.value = product.price;
  elements.editProductStock.value = product.stock;
  elements.editProductCategory.value = product.category;

  // Show modal
  elements.editModal.classList.remove("hidden");

  // Focus on name input
  elements.editProductName.focus();
}

function closeEditModal() {
  elements.editModal.classList.add("hidden");
  elements.editProductForm.reset();
}

function saveProductEdit(event) {
  event.preventDefault();

  const productId = parseInt(elements.editProductId.value);
  const name = elements.editProductName.value.trim();
  const price = parseFloat(elements.editProductPrice.value);
  const stock = parseInt(elements.editProductStock.value);
  const category = elements.editProductCategory.value;

  // Validate data
  if (!name || name.length < 2) {
    showToast("Please enter a valid product name", "error");
    return;
  }

  if (isNaN(price) || price <= 0) {
    showToast("Price must be greater than 0", "error");
    return;
  }

  if (isNaN(stock) || stock < 0) {
    showToast("Stock cannot be negative", "error");
    return;
  }

  // Find and update the product
  const productIndex = appState.products.findIndex((p) => p.id === productId);

  if (productIndex === -1) {
    showToast("Product not found", "error");
    return;
  }

  // Update product data
  appState.products[productIndex] = {
    ...appState.products[productIndex],
    name: name,
    price: price,
    stock: stock,
    category: category,
  };

  // Save to localStorage
  saveToLocalStorage();

  // Update UI
  populateCategoryFilter();
  applyFiltersAndSort();
  updateAnalytics();

  // Close modal
  closeEditModal();

  // Show success message
  showToast(`Product "${name}" updated successfully!`, "success");
}

// 13. Form Validation Helpers

function showFieldError(field, message) {
  const errorElement = document.getElementById(`${field}-error`);
  const inputElement = document.getElementById(`product-${field}`);

  if (errorElement) {
    errorElement.textContent = message;
  }

  if (inputElement) {
    inputElement.classList.add("error");
  }
}

function clearFormErrors() {
  // Clear error messages
  elements.nameError.textContent = "";
  elements.priceError.textContent = "";
  elements.stockError.textContent = "";
  elements.categoryError.textContent = "";

  // Remove error class from inputs
  elements.productName.classList.remove("error");
  elements.productPrice.classList.remove("error");
  elements.productStock.classList.remove("error");
  elements.productCategory.classList.remove("error");
}

// 14. Toast Notification System

function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;

  // Choose icon based on type
  let icon = "✓";
  if (type === "error") icon = "✕";
  if (type === "warning") icon = "⚠";

  toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-message">${escapeHTML(message)}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;

  // Add toast to container
  elements.toastContainer.appendChild(toast);

  // Auto-remove after 4 seconds
  setTimeout(() => {
    if (toast.parentElement) {
      toast.style.animation = "slideOutRight 0.3s ease forwards";
      setTimeout(() => toast.remove(), 300);
    }
  }, 4000);
}

// 15. Event Listeners Setup

function setupEventListeners() {
  // Search input - real-time filtering with debounce
  let searchTimeout;
  elements.searchInput.addEventListener("input", (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      appState.searchQuery = e.target.value;
      applyFiltersAndSort();

      // Show/hide clear button
      elements.clearSearchBtn.classList.toggle("hidden", !e.target.value);
    }, 300); // Debounce for 300ms
  });

  // Clear search button
  elements.clearSearchBtn.addEventListener("click", () => {
    elements.searchInput.value = "";
    appState.searchQuery = "";
    elements.clearSearchBtn.classList.add("hidden");
    applyFiltersAndSort();
  });

  // Category filter change
  elements.categoryFilter.addEventListener("change", (e) => {
    appState.categoryFilter = e.target.value;
    applyFiltersAndSort();
  });

  // Stock filter change
  elements.stockFilter.addEventListener("change", (e) => {
    appState.stockFilter = e.target.value;
    applyFiltersAndSort();
  });

  // Sort select change
  elements.sortSelect.addEventListener("change", (e) => {
    appState.sortOption = e.target.value;
    applyFiltersAndSort();
  });

  // Pagination buttons
  elements.prevPageBtn.addEventListener("click", goToPreviousPage);
  elements.nextPageBtn.addEventListener("click", goToNextPage);

  // Add product form submission
  elements.addProductForm.addEventListener("submit", addProduct);

  // Clear form errors when user starts typing
  elements.productName.addEventListener("input", () => {
    elements.nameError.textContent = "";
    elements.productName.classList.remove("error");
  });
  elements.productPrice.addEventListener("input", () => {
    elements.priceError.textContent = "";
    elements.productPrice.classList.remove("error");
  });
  elements.productStock.addEventListener("input", () => {
    elements.stockError.textContent = "";
    elements.productStock.classList.remove("error");
  });
  elements.productCategory.addEventListener("change", () => {
    elements.categoryError.textContent = "";
    elements.productCategory.classList.remove("error");
  });

  // Edit modal event listeners
  elements.closeModalBtn.addEventListener("click", closeEditModal);
  elements.cancelEditBtn.addEventListener("click", closeEditModal);
  elements.editProductForm.addEventListener("submit", saveProductEdit);

  // Close modal when clicking backdrop
  elements.editModal
    .querySelector(".modal-backdrop")
    .addEventListener("click", closeEditModal);

  // Close modal with Escape key
  document.addEventListener("keydown", (e) => {
    if (
      e.key === "Escape" &&
      !elements.editModal.classList.contains("hidden")
    ) {
      closeEditModal();
    }
  });
}

// 16. Application Entry Point

document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  initializeApp();
});

// 17. Global Function Exports (for onclick handlers)

window.deleteProduct = deleteProduct;
window.openEditModal = openEditModal;
