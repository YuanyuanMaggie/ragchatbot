// API base URL - use relative path to work from any host
const API_URL = '/api';

// Widget State
const widgetState = {
    isExpanded: false,
    isSidebarOpen: false,
    sessionId: null,
    unreadCount: 0
};

// DOM elements
let chatWidgetButton, widgetContainer, closeWidgetButton;
let chatMessages, chatInput, sendButton, newChatButton;
let totalSections, profileHighlights;
let themeToggle, sidebarToggle, widgetSidebar;
let notificationBadge;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    chatWidgetButton = document.getElementById('chatWidgetButton');
    widgetContainer = document.getElementById('widgetContainer');
    closeWidgetButton = document.getElementById('closeWidgetButton');
    chatMessages = document.getElementById('chatMessages');
    chatInput = document.getElementById('chatInput');
    sendButton = document.getElementById('sendButton');
    newChatButton = document.getElementById('newChatButton');
    totalSections = document.getElementById('totalSections');
    profileHighlights = document.getElementById('profileHighlights');
    themeToggle = document.getElementById('themeToggle');
    sidebarToggle = document.getElementById('sidebarToggle');
    widgetSidebar = document.getElementById('widgetSidebar');
    notificationBadge = document.getElementById('notificationBadge');

    setupEventListeners();
    initializeTheme();
    createNewSession();

    // Check if widget should auto-open (from localStorage)
    const autoOpen = localStorage.getItem('widgetAutoOpen') === 'true';
    if (autoOpen) {
        openWidget();
    }
});

// ============================
// EVENT LISTENERS
// ============================

function setupEventListeners() {
    // Widget toggle
    chatWidgetButton.addEventListener('click', openWidget);
    closeWidgetButton.addEventListener('click', closeWidget);

    // Chat functionality
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // New chat button
    newChatButton.addEventListener('click', startNewChat);

    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);

    // Sidebar toggle
    sidebarToggle.addEventListener('click', toggleSidebar);

    // ESC key to close widget
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && widgetState.isExpanded) {
            closeWidget();
        }
    });

    // Suggested questions
    document.querySelectorAll('.suggested-item').forEach(button => {
        button.addEventListener('click', (e) => {
            const question = e.target.getAttribute('data-question');
            chatInput.value = question;
            sendMessage();
        });
    });

    // Click outside sidebar to close it on mobile
    widgetContainer.addEventListener('click', (e) => {
        if (widgetState.isSidebarOpen &&
            !widgetSidebar.contains(e.target) &&
            !sidebarToggle.contains(e.target) &&
            window.innerWidth <= 768) {
            closeSidebar();
        }
    });
}

// ============================
// WIDGET TOGGLE FUNCTIONS
// ============================

function openWidget() {
    widgetState.isExpanded = true;
    widgetContainer.classList.add('expanded');
    chatWidgetButton.classList.add('hidden');

    // Focus input field
    setTimeout(() => {
        chatInput.focus();
    }, 300);

    // Load profile stats if not loaded yet
    if (totalSections.textContent === '-') {
        loadProfileStats();
    }

    // Clear notification badge
    widgetState.unreadCount = 0;
    updateNotificationBadge();

    // Save state
    localStorage.setItem('widgetAutoOpen', 'false');
}

function closeWidget() {
    widgetState.isExpanded = false;
    widgetContainer.classList.remove('expanded');
    chatWidgetButton.classList.remove('hidden');

    // Close sidebar if open
    if (widgetState.isSidebarOpen) {
        closeSidebar();
    }

    // Save state
    localStorage.setItem('widgetAutoOpen', 'false');
}

function toggleWidget() {
    if (widgetState.isExpanded) {
        closeWidget();
    } else {
        openWidget();
    }
}

// ============================
// SIDEBAR TOGGLE FUNCTIONS
// ============================

function toggleSidebar() {
    if (widgetState.isSidebarOpen) {
        closeSidebar();
    } else {
        openSidebar();
    }
}

function openSidebar() {
    widgetState.isSidebarOpen = true;
    widgetSidebar.classList.add('open');

    // Load profile stats if not loaded yet
    if (totalSections.textContent === '-') {
        loadProfileStats();
    }
}

function closeSidebar() {
    widgetState.isSidebarOpen = false;
    widgetSidebar.classList.remove('open');
}

// ============================
// CHAT FUNCTIONS
// ============================

async function sendMessage() {
    const query = chatInput.value.trim();
    if (!query) return;

    // Disable input
    chatInput.value = '';
    chatInput.disabled = true;
    sendButton.disabled = true;

    // Add user message
    addMessage(query, 'user');

    // Add loading message
    const loadingMessage = createLoadingMessage();
    chatMessages.appendChild(loadingMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                session_id: widgetState.sessionId
            })
        });

        if (!response.ok) throw new Error('Query failed');

        const data = await response.json();

        // Update session ID if new
        if (!widgetState.sessionId) {
            widgetState.sessionId = data.session_id;
        }

        // Replace loading message with response
        loadingMessage.remove();
        addMessage(data.answer, 'assistant', data.sources, data.source_links);

    } catch (error) {
        // Replace loading message with error
        loadingMessage.remove();
        addMessage(`Error: ${error.message}`, 'assistant');
    } finally {
        chatInput.disabled = false;
        sendButton.disabled = false;
        chatInput.focus();
    }
}

function createLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="loading">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    return messageDiv;
}

function addMessage(content, type, sources = null, sourceLinks = null, isWelcome = false) {
    const messageId = Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}${isWelcome ? ' welcome-message' : ''}`;
    messageDiv.id = `message-${messageId}`;

    // Convert markdown to HTML for assistant messages
    const displayContent = type === 'assistant' ? marked.parse(content) : escapeHtml(content);

    let html = `<div class="message-content">${displayContent}</div>`;

    if (sources && sources.length > 0) {
        // Create sources with clickable links when available
        const sourcesHtml = sources.map((source, index) => {
            const link = sourceLinks && sourceLinks[index];
            if (link) {
                return `<a href="${link}" target="_blank" class="source-link">${source}</a>`;
            } else {
                return source;
            }
        }).join(', ');

        html += `
            <details class="sources-collapsible">
                <summary class="sources-header">Sources</summary>
                <div class="sources-content">${sourcesHtml}</div>
            </details>
        `;
    }

    messageDiv.innerHTML = html;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // If widget is closed and it's an assistant message, increment unread count
    if (!widgetState.isExpanded && type === 'assistant' && !isWelcome) {
        widgetState.unreadCount++;
        updateNotificationBadge();
    }

    return messageId;
}

// Helper function to escape HTML for user messages
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function startNewChat() {
    // Clear the current session on backend if exists
    if (widgetState.sessionId) {
        try {
            await fetch(`${API_URL}/clear-session`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: widgetState.sessionId
                })
            });
        } catch (error) {
            console.error('Error clearing session:', error);
        }
    }

    // Clear frontend state and UI
    await createNewSession();
}

async function createNewSession() {
    widgetState.sessionId = null;
    chatMessages.innerHTML = '';
    chatInput.value = '';
    chatInput.disabled = false;
    sendButton.disabled = false;
    addMessage('Welcome! I\'m here to help you learn about Yuanyuan Li\'s professional background, experience, and expertise. Ask me anything about her work history, projects, skills, or leadership style.', 'assistant', null, null, true);
}

// ============================
// PROFILE STATS
// ============================

async function loadProfileStats() {
    try {
        console.log('Loading profile stats...');
        const response = await fetch(`${API_URL}/profile-stats`);
        if (!response.ok) throw new Error('Failed to load profile stats');

        const data = await response.json();
        console.log('Profile data received:', data);

        // Update stats in UI
        if (totalSections) {
            totalSections.textContent = data.total_sections;
        }

        // Update profile highlights
        if (profileHighlights) {
            if (data.key_highlights && data.key_highlights.length > 0) {
                profileHighlights.innerHTML = data.key_highlights
                    .map(highlight => `<div class="profile-highlight-item">• ${highlight}</div>`)
                    .join('');
            } else {
                profileHighlights.innerHTML = '<span class="no-profile">No profile data available</span>';
            }
        }

    } catch (error) {
        console.error('Error loading profile stats:', error);
        // Set default values on error
        if (totalSections) {
            totalSections.textContent = '0';
        }
        if (profileHighlights) {
            profileHighlights.innerHTML = '<span class="error">Failed to load profile data</span>';
        }
    }
}

// ============================
// THEME FUNCTIONS
// ============================

function initializeTheme() {
    // Get saved theme preference or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

function setTheme(theme) {
    if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        themeToggle.setAttribute('aria-label', 'Switch to dark theme');
    } else {
        document.documentElement.removeAttribute('data-theme');
        themeToggle.setAttribute('aria-label', 'Switch to light theme');
    }

    // Save theme preference
    localStorage.setItem('theme', theme);
}

// ============================
// NOTIFICATION BADGE
// ============================

function updateNotificationBadge() {
    if (widgetState.unreadCount > 0) {
        notificationBadge.textContent = widgetState.unreadCount > 9 ? '9+' : widgetState.unreadCount;
        notificationBadge.style.display = 'flex';
    } else {
        notificationBadge.style.display = 'none';
    }
}

// ============================
// WIDGET EMBEDDING API (Optional)
// ============================

// Expose a global API for embedding configuration
window.RagChatWidget = {
    open: openWidget,
    close: closeWidget,
    toggle: toggleWidget,
    sendMessage: (message) => {
        if (!widgetState.isExpanded) {
            openWidget();
        }
        setTimeout(() => {
            chatInput.value = message;
            sendMessage();
        }, 300);
    },
    configure: (options) => {
        // Allow external configuration
        if (options.apiUrl) {
            // Would need to make API_URL configurable
            console.log('Custom API URL:', options.apiUrl);
        }
        if (options.theme) {
            setTheme(options.theme);
        }
        if (options.autoOpen) {
            openWidget();
        }
    }
};
