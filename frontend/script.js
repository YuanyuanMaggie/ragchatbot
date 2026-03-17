// API base URL - use relative path to work from any host
const API_URL = '/api';

// Global state
let currentSessionId = null;

// DOM elements
let chatMessages, chatInput, sendButton, totalSections, profileHighlights, newChatButton, themeToggle;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements after page loads
    chatMessages = document.getElementById('chatMessages');
    chatInput = document.getElementById('chatInput');
    sendButton = document.getElementById('sendButton');
    totalSections = document.getElementById('totalSections');
    profileHighlights = document.getElementById('profileHighlights');
    newChatButton = document.getElementById('newChatButton');
    themeToggle = document.getElementById('themeToggle');

    setupEventListeners();
    initializeTheme();
    createNewSession();
    loadProfileStats();
});

// Event Listeners
function setupEventListeners() {
    // Chat functionality
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    // New chat button
    newChatButton.addEventListener('click', startNewChat);
    
    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);
    
    // Keyboard shortcut for theme toggle (Ctrl/Cmd + Shift + T)
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
            e.preventDefault();
            toggleTheme();
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
}


// Chat Functions
async function sendMessage() {
    const query = chatInput.value.trim();
    if (!query) return;

    // Disable input
    chatInput.value = '';
    chatInput.disabled = true;
    sendButton.disabled = true;

    // Add user message
    addMessage(query, 'user');

    // Add loading message - create a unique container for it
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
                session_id: currentSessionId
            })
        });

        if (!response.ok) throw new Error('Query failed');

        const data = await response.json();
        
        // Update session ID if new
        if (!currentSessionId) {
            currentSessionId = data.session_id;
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
    
    return messageId;
}

// Helper function to escape HTML for user messages
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Removed removeMessage function - no longer needed since we handle loading differently

async function startNewChat() {
    // Clear the current session on backend if exists
    if (currentSessionId) {
        try {
            await fetch(`${API_URL}/clear-session`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: currentSessionId
                })
            });
        } catch (error) {
            console.error('Error clearing session:', error);
            // Continue with frontend cleanup even if backend fails
        }
    }
    
    // Clear frontend state and UI
    await createNewSession();
}

async function createNewSession() {
    currentSessionId = null;
    chatMessages.innerHTML = '';
    chatInput.value = '';
    chatInput.disabled = false;
    sendButton.disabled = false;
    addMessage('Welcome! I\'m here to help you learn about Yuanyuan Li\'s professional background, experience, and expertise. Ask me anything about her work history, projects, skills, or leadership style.', 'assistant', null, null, true);
}

// Load profile statistics
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

// Theme Functions
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