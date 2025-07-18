// Modern Chat Interface JavaScript with LangGraph Memory Support
class TravelPlannerChat {
  constructor() {
    this.chatForm = document.getElementById("chat-form");
    this.userInput = document.getElementById("user-input");
    this.chatBox = document.getElementById("chatbox");
    this.sendBtn = document.getElementById("send-btn");
    this.downloadBtn = document.getElementById("download-btn");
    this.clearChatBtn = document.getElementById("clear-chat-btn");
    this.typingIndicator = document.getElementById("typing-indicator");
    this.charCount = document.getElementById("char-count");
    this.errorModal = document.getElementById("error-modal");
    this.closeErrorModal = document.getElementById("close-error-modal");
    this.cancelErrorModal = document.getElementById("cancel-error-modal");
    this.retryBtn = document.getElementById("retry-btn");
    this.loadingScreen = document.getElementById("loading-screen");
    this.mainApp = document.getElementById("main-app");
    
    // Session management for LangGraph memory
    this.sessionId = this.getOrCreateSessionId();
    this.chatHistory = this.loadChatHistory();
    this.currentQuery = null;
    this.lastResponse = null; // lastResponse will now be used to check if a plan exists before attempting download
    
    this.init();
  }

  getOrCreateSessionId() {
    let sessionId = localStorage.getItem("travelPlannerSessionId");
    if (!sessionId) {
      sessionId = 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
      localStorage.setItem("travelPlannerSessionId", sessionId);
    }
    return sessionId;
  }

  init() {
    // Show loading screen initially, then transition to main app
    this.showLoadingScreen();
    
    // Initialize app after a brief delay to show loading animation
    setTimeout(() => {
      this.hideLoadingScreen();
      this.setupEventListeners();
      this.loadChatHistory();
      this.updateWelcomeTime();
      this.userInput.focus();
    }, 1500);
  }

  setupEventListeners() {
    // Form submission
    this.chatForm.addEventListener("submit", (e) => this.handleSubmit(e));
    
    // Input events
    this.userInput.addEventListener("input", () => this.handleInputChange());
    this.userInput.addEventListener("keydown", (e) => this.handleKeyDown(e));
    
    // Button events
    this.clearChatBtn.addEventListener("click", () => this.clearChat());
    this.downloadBtn.addEventListener("click", () => this.downloadPDF());
    if (this.closeErrorModal) this.closeErrorModal.addEventListener("click", () => this.hideErrorModal());
    if (this.cancelErrorModal) this.cancelErrorModal.addEventListener("click", () => this.hideErrorModal());
    if (this.retryBtn) this.retryBtn.addEventListener("click", () => this.retryLastQuery());
    
    // Example button events
    document.addEventListener("click", (e) => {
      if (e.target.classList.contains("example-btn")) {
        const query = e.target.getAttribute("data-query");
        if (query) {
          this.userInput.value = query;
          this.handleInputChange();
          this.handleSubmit(new Event('submit'));
        }
      }
    });
    
    // Modal events (if error modal exists)
    if (this.errorModal) {
      this.errorModal.addEventListener("click", (e) => {
        if (e.target === this.errorModal) this.hideErrorModal();
      });
    }

    // Escape key to close modal
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.errorModal && this.errorModal.classList.contains("visible")) {
        this.hideErrorModal();
      }
    });
  }

  handleInputChange() {
    const value = this.userInput.value;
    const length = value.length;
    
    // Update character count if element exists
    if (this.charCount) {
      this.charCount.textContent = `${length}/500`;
      
      // Color coding for character count
      if (length > 450) {
        this.charCount.style.color = "#dc2626"; // Red
      } else if (length > 400) {
        this.charCount.style.color = "#f59e0b"; // Orange
      } else {
        this.charCount.style.color = "#6b7280"; // Gray
      }
    }
    
    // Enable/disable send button
    if (this.sendBtn) {
      this.sendBtn.disabled = length === 0 || length > 500;
    }
  }

  handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      this.handleSubmit(e);
    }
  }

  async handleSubmit(e) {
    e.preventDefault();
    
    const question = this.userInput.value.trim();
    if (!question || question.length > 500) return;

    this.currentQuery = question;
    
    // Add user message
    this.addMessage("user", question);
    this.saveToHistory("user", question);
    
    // Clear input and disable form
    this.userInput.value = "";
    this.handleInputChange();
    this.setFormDisabled(true);
    
    // Show typing indicator
    this.showTypingIndicator();
    
    try {
      await this.sendQuery(question);
    } catch (error) {
      this.handleError(error);
    } finally {
      this.hideTypingIndicator();
      this.setFormDisabled(false);
      this.userInput.focus();
    }
  }

  async sendQuery(question) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout
    
    try {
      // Define your backend URL. For local development, it's usually http://localhost:8000
      // For deployment, this should be an environment variable or configured dynamically.
      const BASE_URL = window.location.origin; 

      const response = await fetch(`${BASE_URL}/query`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({ 
          question: question,
          session_id: this.sessionId 
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      
      // Update session ID if a new one was created
      if (result.session_id) {
        this.sessionId = result.session_id;
        localStorage.setItem("travelPlannerSessionId", this.sessionId);
      }
      
      if (!result.answer) {
        throw new Error("No answer received from the server");
      }

      this.lastResponse = result.answer; // Store the last response to check if a plan exists for download
      this.addMessage("bot", result.answer);
      this.saveToHistory("bot", result.answer);
      this.showDownloadButton();
      
    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error.name === 'AbortError') {
        throw new Error("Request timed out. Please try again.");
      } else if (error.message.includes('Failed to fetch')) {
        throw new Error("Unable to connect to the travel planner service. Please check if the server is running.");
      } else {
        throw error;
      }
    }
  }

  addMessage(sender, text) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message " + (sender === "user" ? "user-message" : "bot-message");
    
    const timestamp = this.formatTime(new Date());
    
    messageDiv.innerHTML = `
      <div class="message-avatar">
        <i class="fas ${sender === "user" ? "fa-user" : "fa-robot"}"></i>
      </div>
      <div class="message-content">
        <div class="message-text">${this.formatMessage(text)}</div>
        <div class="message-time">${timestamp}</div>
      </div>
    `;
    
    // Remove welcome message if it's the first user message
    if (sender === "user" && this.chatBox.querySelector(".welcome-message")) {
      this.chatBox.querySelector(".welcome-message").remove();
    }
    
    this.chatBox.appendChild(messageDiv);
    this.scrollToBottom();
  }

  formatMessage(text) {
    // Basic markdown-like formatting
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>')
      .replace(/#{1,6}\s(.*?)(?=\n|$)/g, '<strong>$1</strong>')
      .replace(/- (.*?)(?=\n|$)/g, '• $1');
  }

  formatTime(date) {
    return date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true 
    });
  }

  updateWelcomeTime() {
    const welcomeTime = document.getElementById("welcome-time");
    if (welcomeTime) {
      welcomeTime.textContent = this.formatTime(new Date());
    }
  }

  showTypingIndicator() {
    if (this.typingIndicator) {
      this.typingIndicator.style.display = "block";
      this.scrollToBottom();
    }
  }

  hideTypingIndicator() {
    if (this.typingIndicator) {
      this.typingIndicator.style.display = "none";
    }
  }

  setFormDisabled(disabled) {
    this.userInput.disabled = disabled;
    if (this.sendBtn) {
      this.sendBtn.disabled = disabled || this.userInput.value.trim().length === 0;
    }
    
    if (disabled) {
      this.userInput.placeholder = "Please wait...";
    } else {
      this.userInput.placeholder = "Plan a trip to Goa for 5 days with a medium budget...";
    }
  }

  scrollToBottom() {
    // Use requestAnimationFrame for smooth scrolling
    requestAnimationFrame(() => {
      this.chatBox.scrollTop = this.chatBox.scrollHeight;
    });
  }

  showDownloadButton() {
    // Only show download button if there's a last response (i.e., a plan has been generated)
    if (this.downloadBtn && this.lastResponse) {
      this.downloadBtn.style.display = "flex";
    }
  }

  async downloadPDF() {
    if (!this.lastResponse) {
      this.showError("No travel plan available to download. Please generate a plan first.");
      return;
    }

    try {
      const BASE_URL = window.location.origin; // Ensure this matches your backend URL
      const response = await fetch(`${BASE_URL}/generate-pdf/${this.sessionId}`);

      if (!response.ok) {
        throw new Error(`Failed to generate PDF: ${response.status} ${response.statusText}`);
      }

      // Get the PDF blob and create a download link
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement("a");
      link.href = url;
      link.download = `travel_plan_${new Date().toISOString().split('T')[0]}.pdf`; // Suggest a PDF filename
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      URL.revokeObjectURL(url); // Clean up the object URL

      // No need to add a message to chatbox, browser will handle download notification
      // this.addMessage("bot", "📥 Your travel plan has been downloaded successfully!");
      // this.saveToHistory("bot", "📥 Your travel plan has been downloaded successfully!");
      
    } catch (error) {
      console.error("Download error:", error);
      this.showError("Failed to download the travel plan. Please ensure the backend is running and a plan has been generated.");
    }
  }

  async clearChat() {
    // Replaced confirm() with a custom modal for better UX
    this.showConfirmationModal("Are you sure you want to clear the chat history? This will start a new conversation session.", async () => {
      try {
        // Clear session on backend using LangGraph memory
        const BASE_URL = window.location.origin; // Ensure this matches your backend URL
        const response = await fetch(`${BASE_URL}/clear-session`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: this.sessionId }),
        });

        if (response.ok) {
          // Clear frontend chat
          this.chatHistory = [];
          this.lastResponse = null;
          this.saveChatHistory();
          
          // Generate new session ID
          this.sessionId = 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
          localStorage.setItem("travelPlannerSessionId", this.sessionId);
          
          // Clear chat box and restore welcome message
          this.chatBox.innerHTML = `
            <div class="welcome-message">
              <div class="message bot-message">
                <div class="message-avatar">
                  <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                  <div class="message-text">
                    <div class="welcome-header">
                      <h2>👋 Welcome to AI Travel Planner!</h2>
                      <p>I'm your personal travel assistant, ready to help you create amazing experiences.</p>
                    </div>
                    
                    <div class="features-grid">
                      <div class="feature-card">
                        <i class="fas fa-route"></i>
                        <span>Day-by-day itineraries</span>
                      </div>
                      <div class="feature-card">
                        <i class="fas fa-hotel"></i>
                        <span>Hotel recommendations</span>
                      </div>
                      <div class="feature-card">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>Local attractions</span>
                      </div>
                      <div class="feature-card">
                        <i class="fas fa-utensils"></i>
                        <span>Restaurant suggestions</span>
                      </div>
                      <div class="feature-card">
                        <i class="fas fa-car"></i>
                        <span>Transportation options</span>
                      </div>
                      <div class="feature-card">
                        <i class="fas fa-calculator"></i>
                        <span>Budget breakdowns</span>
                      </div>
                    </div>
                    
                    <div class="cta-section">
                      <p><strong>Ready to start planning?</strong></p>
                      <p>Tell me where you'd like to go and for how long!</p>
                      <div class="example-queries">
                        <button class="example-btn" data-query="Plan a 7-day romantic trip to Paris for 2 people with a budget of $3000">
                          Paris Romance ✨
                        </button>
                        <button class="example-btn" data-query="Create a 5-day adventure itinerary for Bali on a moderate budget">
                          Bali Adventure 🏄‍♀️
                        </button>
                        <button class="example-btn" data-query="Plan a family-friendly 4-day trip to Tokyo with kids">
                          Tokyo Family Fun 👨‍👩‍👧‍👦
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="message-time" id="welcome-time">${this.formatTime(new Date())}</div>
                </div>
              </div>
            </div>
          `;
          
          if (this.downloadBtn) this.downloadBtn.style.display = "none";
          this.userInput.focus();
        } else {
          console.error("Failed to clear session on backend");
          this.showError("Failed to clear session. Please try again.");
        }
      } catch (err) {
        console.error("Error clearing chat:", err);
        this.showError("Error clearing chat. Please try again.");
      }
    });
  }

  handleError(error) {
    console.error("Chat error:", error);
    this.showError(error.message || "An unexpected error occurred. Please try again.");
  }

  showError(message) {
    if (this.errorModal) {
      const errorMessageEl = document.getElementById("error-message");
      if (errorMessageEl) {
        errorMessageEl.textContent = message;
      }
      this.errorModal.classList.add("visible");
    } else {
      // Fallback if no error modal
      // Using a custom alert for consistency, as alert() is not allowed in Canvas
      this.showCustomAlert(message, "Error");
    }
  }

  hideErrorModal() {
    if (this.errorModal) {
      this.errorModal.classList.remove("visible");
    }
  }

  retryLastQuery() {
    this.hideErrorModal();
    if (this.currentQuery) {
      this.userInput.value = this.currentQuery;
      this.handleInputChange();
      this.handleSubmit(new Event('submit'));
    }
  }

  saveToHistory(sender, text) {
    this.chatHistory.push({
      sender,
      text,
      timestamp: new Date().toISOString(),
      sessionId: this.sessionId
    });
    this.saveChatHistory();
  }

  loadChatHistory() {
    try {
      const saved = localStorage.getItem("travelPlannerChatHistory");
      this.chatHistory = saved ? JSON.parse(saved) : [];
      
      // Filter history by current session to maintain session isolation
      const sessionHistory = this.chatHistory.filter(msg => 
        msg.sessionId === this.sessionId || !msg.sessionId // Include old messages without sessionId
      );
      
      // Restore messages (limit to last 50 to prevent performance issues)
      const recentHistory = sessionHistory.slice(-50);
      let hasMessages = false;
      
      recentHistory.forEach(msg => {
        if (msg.sender && msg.text) {
          this.addMessageFromHistory(msg.sender, msg.text, msg.timestamp);
          hasMessages = true;
          if (msg.sender === "bot") {
            this.lastResponse = msg.text; // Restore lastResponse from history
          }
        }
      });
      
      if (hasMessages) {
        // Remove welcome message if there are saved messages
        const welcomeMsg = this.chatBox.querySelector(".welcome-message");
        if (welcomeMsg) welcomeMsg.remove();
        this.showDownloadButton();
      }
      
    } catch (error) {
      console.error("Error loading chat history:", error);
      this.chatHistory = [];
    }
  }

  addMessageFromHistory(sender, text, timestamp) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message " + (sender === "user" ? "user-message" : "bot-message");
    
    const time = timestamp ? this.formatTime(new Date(timestamp)) : this.formatTime(new Date());
    
    messageDiv.innerHTML = `
      <div class="message-avatar">
        <i class="fas ${sender === "user" ? "fa-user" : "fa-robot"}"></i>
      </div>
      <div class="message-content">
        <div class="message-text">${this.formatMessage(text)}</div>
        <div class="message-time">${time}</div>
      </div>
    `;
    
    this.chatBox.appendChild(messageDiv);
  }

  saveChatHistory() {
    try {
      // Keep only last 100 messages to prevent localStorage from getting too large
      const limitedHistory = this.chatHistory.slice(-100);
      localStorage.setItem("travelPlannerChatHistory", JSON.stringify(limitedHistory));
    } catch (error) {
      console.error("Error saving chat history:", error);
      // If localStorage is full, clear it and try again
      localStorage.removeItem("travelPlannerChatHistory");
    }
  }

  showLoadingScreen() {
    if (this.loadingScreen) {
      this.loadingScreen.style.display = "flex";
    }
    if (this.mainApp) {
      this.mainApp.style.display = "none";
    }
  }

  hideLoadingScreen() {
    if (this.loadingScreen) {
      this.loadingScreen.classList.add('fade-out');
      setTimeout(() => {
        this.loadingScreen.style.display = "none";
        if (this.mainApp) {
          this.mainApp.style.display = "block";
          this.mainApp.classList.add('visible');
        }
      }, 500);
    }
  }

  // Custom Alert/Confirmation Modals (replacing browser's alert/confirm)
  showCustomAlert(message, title = "Notification") {
    const alertModal = document.createElement("div");
    alertModal.className = "modal visible";
    alertModal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="fas fa-info-circle"></i> ${title}</h3>
          <button class="close-btn custom-alert-close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>${message}</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary custom-alert-ok-btn">OK</button>
        </div>
      </div>
    `;
    document.body.appendChild(alertModal);

    const closeBtn = alertModal.querySelector(".custom-alert-close-btn");
    const okBtn = alertModal.querySelector(".custom-alert-ok-btn");

    const closeAlert = () => {
      alertModal.classList.remove("visible");
      alertModal.addEventListener('transitionend', () => alertModal.remove(), { once: true });
    };

    closeBtn.addEventListener("click", closeAlert);
    okBtn.addEventListener("click", closeAlert);
    alertModal.addEventListener("click", (e) => {
      if (e.target === alertModal) closeAlert();
    });
  }

  showConfirmationModal(message, onConfirm) {
    const confirmModal = document.createElement("div");
    confirmModal.className = "modal visible";
    confirmModal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h3><i class="fas fa-question-circle"></i> Confirm</h3>
          <button class="close-btn custom-confirm-close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>${message}</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary custom-confirm-ok-btn">Yes</button>
          <button class="btn btn-secondary custom-confirm-cancel-btn">No</button>
        </div>
      </div>
    `;
    document.body.appendChild(confirmModal);

    const closeBtn = confirmModal.querySelector(".custom-confirm-close-btn");
    const okBtn = confirmModal.querySelector(".custom-confirm-ok-btn");
    const cancelBtn = confirmModal.querySelector(".custom-confirm-cancel-btn");

    const closeConfirm = () => {
      confirmModal.classList.remove("visible");
      confirmModal.addEventListener('transitionend', () => confirmModal.remove(), { once: true });
    };

    okBtn.addEventListener("click", () => {
      onConfirm();
      closeConfirm();
    });
    cancelBtn.addEventListener("click", closeConfirm);
    closeBtn.addEventListener("click", closeConfirm);
    confirmModal.addEventListener("click", (e) => {
      if (e.target === confirmModal) closeConfirm();
    });
  }
}

// Initialize the chat when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new TravelPlannerChat();
});

// Handle page visibility change to manage resources
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    // Page is hidden, could pause animations or reduce activity
  } else {
    // Page is visible again
    const userInput = document.getElementById("user-input");
    if (userInput && !userInput.disabled) {
      userInput.focus();
    }
  }
});
