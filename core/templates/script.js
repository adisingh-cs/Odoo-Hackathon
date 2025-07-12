// DOM Elements
const sidebar = document.getElementById("sidebar");
const mobileOverlay = document.getElementById("mobileOverlay");
const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const pageTitle = document.getElementById("pageTitle");
const navItems = document.querySelectorAll(".nav-item[data-page]");
const pageContents = document.querySelectorAll(".page-content[data-content]");
const tabBtns = document.querySelectorAll(".tab-btn[data-tab]");
const tabPanes = document.querySelectorAll(".tab-pane[data-pane]");
const announcementForm = document.getElementById("announcementForm");
const subjectInput = document.getElementById("subject");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");

// State
let currentPage = "admin-panel";
let currentTab = "platform-messages";
let isMobileSidebarOpen = false;

// Page titles mapping
const pageTitles = {
  dashboard: "Dashboard",
  search: "Search",
  "swap-requests": "Swap Requests",
  profile: "Profile",
  messages: "Messages",
  settings: "Settings",
  "admin-panel": "Admin Panel",
};

// Mobile sidebar functionality
function toggleMobileSidebar() {
  isMobileSidebarOpen = !isMobileSidebarOpen;

  if (isMobileSidebarOpen) {
    sidebar.classList.add("open");
    mobileOverlay.classList.add("active");
    document.body.style.overflow = "hidden";
  } else {
    sidebar.classList.remove("open");
    mobileOverlay.classList.remove("active");
    document.body.style.overflow = "";
  }
}

function closeMobileSidebar() {
  if (isMobileSidebarOpen) {
    toggleMobileSidebar();
  }
}

// Page navigation
function navigateToPage(page) {
  // Update current page
  currentPage = page;

  // Update page title
  pageTitle.textContent = pageTitles[page] || "Page";

  // Update nav items
  navItems.forEach((item) => {
    item.classList.remove("active");
    if (item.dataset.page === page) {
      item.classList.add("active");
    }
  });

  // Update page content
  pageContents.forEach((content) => {
    content.classList.remove("active");
    if (content.dataset.content === page) {
      content.classList.add("active");
    }
  });

  // Close mobile sidebar
  closeMobileSidebar();
}

// Tab navigation (for admin panel)
function navigateToTab(tab) {
  currentTab = tab;

  // Update tab buttons
  tabBtns.forEach((btn) => {
    btn.classList.remove("active");
    if (btn.dataset.tab === tab) {
      btn.classList.add("active");
    }
  });

  // Update tab panes
  tabPanes.forEach((pane) => {
    pane.classList.remove("active");
    if (pane.dataset.pane === tab) {
      pane.classList.add("active");
    }
  });
}

// Form validation
function validateForm() {
  const subject = subjectInput.value.trim();
  const message = messageInput.value.trim();

  if (subject && message) {
    sendBtn.disabled = false;
  } else {
    sendBtn.disabled = true;
  }
}

// Handle form submission
function handleFormSubmit(e) {
  e.preventDefault();

  const subject = subjectInput.value.trim();
  const message = messageInput.value.trim();

  if (subject && message) {
    // Simulate sending announcement
    console.log("Sending announcement:", { subject, message });

    // Show success message (you can replace this with a proper notification)
    alert("Announcement sent successfully!");

    // Clear form
    subjectInput.value = "";
    messageInput.value = "";
    validateForm();
  }
}

// Handle window resize
function handleResize() {
  if (window.innerWidth > 1024) {
    // Close mobile sidebar on desktop
    if (isMobileSidebarOpen) {
      closeMobileSidebar();
    }
  }
}

// Keyboard navigation
function handleKeyPress(e) {
  // Close sidebar on Escape key
  if (e.key === "Escape" && isMobileSidebarOpen) {
    closeMobileSidebar();
  }

  // Submit form on Ctrl+Enter or Cmd+Enter
  if (
    (e.ctrlKey || e.metaKey) &&
    e.key === "Enter" &&
    document.activeElement === messageInput
  ) {
    if (!sendBtn.disabled) {
      handleFormSubmit(e);
    }
  }
}

// Initialize event listeners
function initializeEventListeners() {
  // Mobile menu button
  mobileMenuBtn.addEventListener("click", toggleMobileSidebar);

  // Mobile overlay click
  mobileOverlay.addEventListener("click", closeMobileSidebar);

  // Navigation items
  navItems.forEach((item) => {
    item.addEventListener("click", () => {
      const page = item.dataset.page;
      navigateToPage(page);
    });
  });

  // Tab buttons
  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const tab = btn.dataset.tab;
      navigateToTab(tab);
    });
  });

  // Form inputs
  subjectInput.addEventListener("input", validateForm);
  messageInput.addEventListener("input", validateForm);

  // Form submission
  announcementForm.addEventListener("submit", handleFormSubmit);

  // Window events
  window.addEventListener("resize", handleResize);
  document.addEventListener("keydown", handleKeyPress);

  // Prevent form submission on Enter in subject field
  subjectInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      messageInput.focus();
    }
  });
}

// Auto-resize textarea
function autoResizeTextarea() {
  const textarea = messageInput;
  textarea.style.height = "auto";
  textarea.style.height = Math.min(textarea.scrollHeight, 200) + "px";
}

// Enhanced form functionality
function enhanceFormFunctionality() {
  // Auto-resize message textarea
  messageInput.addEventListener("input", autoResizeTextarea);

  // Character counter (optional)
  const maxLength = 1000;
  messageInput.setAttribute("maxlength", maxLength);

  // Add character counter
  const messageGroup = messageInput.parentElement;
  const charCounter = document.createElement("div");
  charCounter.className = "char-counter";
  charCounter.style.cssText = `
    font-size: 12px;
    color: #737373;
    text-align: right;
    margin-top: 4px;
  `;
  messageGroup.appendChild(charCounter);

  function updateCharCounter() {
    const remaining = maxLength - messageInput.value.length;
    charCounter.textContent = `${remaining} characters remaining`;

    if (remaining < 50) {
      charCounter.style.color = "#ef4444";
    } else if (remaining < 100) {
      charCounter.style.color = "#f59e0b";
    } else {
      charCounter.style.color = "#737373";
    }
  }

  messageInput.addEventListener("input", updateCharCounter);
  updateCharCounter();
}

// Toast notification system
function createToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background-color: ${type === "success" ? "#10b981" : "#ef4444"};
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    font-size: 14px;
    font-weight: 500;
    max-width: 300px;
  `;

  toast.textContent = message;
  document.body.appendChild(toast);

  // Animate in
  setTimeout(() => {
    toast.style.transform = "translateX(0)";
  }, 100);

  // Remove after 3 seconds
  setTimeout(() => {
    toast.style.transform = "translateX(100%)";
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, 3000);
}

// Enhanced form submission with toast
function enhancedFormSubmit(e) {
  e.preventDefault();

  const subject = subjectInput.value.trim();
  const message = messageInput.value.trim();

  if (subject && message) {
    // Simulate API call with loading state
    sendBtn.disabled = true;
    sendBtn.textContent = "Sending...";

    setTimeout(() => {
      console.log("Sending announcement:", { subject, message });

      // Show success toast
      createToast("Announcement sent successfully!");

      // Clear form
      subjectInput.value = "";
      messageInput.value = "";
      validateForm();

      // Reset button
      sendBtn.textContent = "Send Announcement";
    }, 1000);
  }
}

// Local storage for draft saving
function saveDraft() {
  const draft = {
    subject: subjectInput.value,
    message: messageInput.value,
    timestamp: Date.now(),
  };
  localStorage.setItem("announcement_draft", JSON.stringify(draft));
}

function loadDraft() {
  const draftStr = localStorage.getItem("announcement_draft");
  if (draftStr) {
    try {
      const draft = JSON.parse(draftStr);
      // Only load if draft is less than 24 hours old
      if (Date.now() - draft.timestamp < 24 * 60 * 60 * 1000) {
        subjectInput.value = draft.subject || "";
        messageInput.value = draft.message || "";
        validateForm();
      }
    } catch (e) {
      console.warn("Could not load draft:", e);
    }
  }
}

function clearDraft() {
  localStorage.removeItem("announcement_draft");
}

// Initialize draft functionality
function initializeDraftSaving() {
  loadDraft();

  let draftTimer;
  function scheduleAutoSave() {
    clearTimeout(draftTimer);
    draftTimer = setTimeout(saveDraft, 1000);
  }

  subjectInput.addEventListener("input", scheduleAutoSave);
  messageInput.addEventListener("input", scheduleAutoSave);

  // Clear draft on successful submission
  announcementForm.addEventListener("submit", () => {
    setTimeout(clearDraft, 1000);
  });
}

// Smooth scrolling for mobile tabs
function smoothScrollTabs() {
  const tabsContainer = document.querySelector(".admin-tabs");
  if (tabsContainer) {
    tabsContainer.addEventListener("wheel", (e) => {
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
        e.preventDefault();
        tabsContainer.scrollLeft += e.deltaX;
      }
    });
  }
}

// Initialize everything when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  initializeEventListeners();
  enhanceFormFunctionality();
  initializeDraftSaving();
  smoothScrollTabs();

  // Replace the simple form submit with enhanced version
  announcementForm.removeEventListener("submit", handleFormSubmit);
  announcementForm.addEventListener("submit", enhancedFormSubmit);

  console.log("SkillExchange Admin Panel initialized successfully!");
});

// Export functions for potential external use
window.SkillExchangeAdmin = {
  navigateToPage,
  navigateToTab,
  toggleMobileSidebar,
  createToast,
};
