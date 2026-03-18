# Chat Widget - Usage Guide

This document explains how to use and embed the Yuanyuan Li Profile Chat Widget on your website.

## Overview

The chat widget provides a floating, collapsible interface for interacting with Yuanyuan Li's professional profile chatbot. It appears as a small button in the corner of your page and expands into a full chat interface when clicked.

## Files

- **widget.html** - Standalone widget HTML page
- **widget.css** - Widget-specific styles
- **widget.js** - Widget functionality and interactions

## Features

### Core Functionality
- **Floating Button**: Clickable chat icon in the bottom-right corner
- **Expandable Chat**: Opens to 420px × 650px chat interface
- **Collapsible Sidebar**: Access profile stats and suggested questions
- **Theme Toggle**: Switch between light and dark themes
- **Session Persistence**: Maintains conversation history
- **Responsive Design**: Full-screen on mobile, optimized for all devices
- **Notification Badge**: Shows unread message count (when implemented)

### User Interactions
- Click floating button to open widget
- Click X button to close widget
- Press ESC key to close widget
- Click sidebar icon to view profile information
- Click theme icon to toggle light/dark mode
- Click + icon to start a new chat session

## Usage Options

### Option 1: Standalone Widget Page (Simplest)

Access the widget directly at:
```
http://localhost:8000/widget.html
```

This is ideal for:
- Testing the widget
- Using as a standalone chat interface
- Embedding in an iframe

### Option 2: Direct Embedding (Recommended)

Embed the widget files directly in your website:

#### Step 1: Add the HTML to your page

```html
<!-- Add this near the closing </body> tag -->

<!-- Floating Chat Button -->
<button id="chatWidgetButton" class="chat-widget-button" aria-label="Open chat">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>
    <span id="notificationBadge" class="notification-badge" style="display: none;">0</span>
</button>

<!-- Widget Container (copy full structure from widget.html) -->
<div id="widgetContainer" class="widget-container">
    <!-- Copy the entire widget-container contents from widget.html -->
</div>

<!-- Include dependencies -->
<link rel="stylesheet" href="http://localhost:8000/widget.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="http://localhost:8000/widget.js"></script>
```

#### Step 2: Configure (Optional)

```javascript
<script>
// Configure the widget after page loads
document.addEventListener('DOMContentLoaded', () => {
    if (window.RagChatWidget) {
        window.RagChatWidget.configure({
            theme: 'dark',        // 'light' or 'dark'
            autoOpen: false       // Open widget automatically
        });
    }
});
</script>
```

### Option 3: Iframe Embedding (Better Isolation)

Embed using an iframe for complete style isolation:

```html
<iframe
    src="http://localhost:8000/widget.html"
    id="ragchat-widget-frame"
    style="position: fixed;
           bottom: 0;
           right: 0;
           width: 100%;
           height: 100%;
           border: none;
           pointer-events: none;
           z-index: 999;">
</iframe>

<style>
/* Ensure iframe doesn't block clicks on parent page */
#ragchat-widget-frame {
    pointer-events: none;
}

/* Enable clicks only on the widget elements */
#ragchat-widget-frame.active {
    pointer-events: all;
}
</style>

<script>
// Optional: Add logic to enable pointer events when widget is active
const iframe = document.getElementById('ragchat-widget-frame');
iframe.addEventListener('load', () => {
    // You can communicate with the iframe if needed
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    // Enable pointer events on widget button and container
    iframe.style.pointerEvents = 'all';
});
</script>
```

**Note**: Iframe approach requires configuring pointer-events carefully to avoid blocking clicks on the parent page.

## JavaScript API

The widget exposes a global `RagChatWidget` API:

```javascript
// Open the widget
window.RagChatWidget.open();

// Close the widget
window.RagChatWidget.close();

// Toggle widget (open/close)
window.RagChatWidget.toggle();

// Send a message programmatically
window.RagChatWidget.sendMessage("Tell me about Yuanyuan's experience");

// Configure widget options
window.RagChatWidget.configure({
    apiUrl: '/api',       // Custom API endpoint (optional)
    theme: 'light',       // 'light' or 'dark'
    autoOpen: true        // Auto-open on page load
});
```

### Example: Trigger Widget from External Button

```html
<button onclick="window.RagChatWidget.open()">
    Chat with Yuanyuan's Profile
</button>

<button onclick="window.RagChatWidget.sendMessage('What are your key achievements?')">
    Ask about achievements
</button>
```

## Customization

### Colors and Branding

Edit CSS variables in [widget.css](widget.css:1-29):

```css
:root {
    --primary-color: #2563eb;      /* Main brand color */
    --primary-hover: #1d4ed8;      /* Hover state */
    --background: #0f172a;         /* Dark background */
    --surface: #1e293b;            /* Surface color */
    --text-primary: #f1f5f9;       /* Primary text */
    --text-secondary: #94a3b8;     /* Secondary text */
}
```

### Widget Size

Edit dimensions in [widget.css](widget.css:98-101):

```css
.widget-container {
    width: 420px;      /* Change widget width */
    height: 650px;     /* Change widget height */
    bottom: 20px;      /* Distance from bottom */
    right: 20px;       /* Distance from right */
}
```

### Floating Button Position

Edit position in [widget.css](widget.css:30-40):

```css
.chat-widget-button {
    bottom: 20px;      /* Distance from bottom */
    right: 20px;       /* Distance from right */
    /* Change to 'left: 20px' for bottom-left position */
}
```

## Responsive Behavior

### Desktop (> 768px)
- Widget: 420px × 650px
- Positioned bottom-right with margins
- Sidebar slides in from left

### Tablet (≤ 768px)
- Widget: Full screen (100vw × 100vh)
- Sidebar overlays chat area
- Button: Slightly smaller (56px)

### Mobile (≤ 480px)
- Widget: Full screen
- Optimized touch targets
- Smaller fonts and padding
- Sidebar: Full width overlay

## Differences from Full-Page Version

| Feature | Full-Page ([index.html](index.html)) | Widget ([widget.html](widget.html)) |
|---------|--------------------------------------|-------------------------------------|
| Layout | Full viewport with header & sidebar | Floating expandable container |
| Access | Main application page | Embeddable on any page |
| Size | 100vw × 100vh | 420px × 650px (desktop) |
| Header | Full header with title | Compact header with avatar |
| Sidebar | Always visible (320px) | Collapsible, hidden by default |
| Position | Static, fills viewport | Fixed, bottom-right corner |
| Mobile | Responsive layout | Full screen overlay |

## Testing

1. Start the backend server:
```bash
cd backend && uv run uvicorn app:app --reload --port 8000
```

2. Open the widget in your browser:
```
http://localhost:8000/widget.html
```

3. Test interactions:
   - Click floating button to open
   - Send a message
   - Toggle theme (sun/moon icon)
   - Toggle sidebar (three dots icon)
   - Start new chat (+ icon)
   - Close widget (X icon)
   - Press ESC to close

## Deployment

### For Production

1. **Update API URL** in [widget.js](widget.js:2):
```javascript
const API_URL = 'https://your-production-domain.com/api';
```

2. **Bundle and Minify** (optional):
   - Combine CSS and JS into single files
   - Minify for smaller file size
   - Add cache busting with version numbers

3. **CDN Hosting** (recommended):
   - Host widget files on a CDN
   - Update script/link URLs in embedding code
   - Enable CORS on your API server

4. **Security**:
   - Configure CORS properly (don't use `allow_origins=["*"]` in production)
   - Add rate limiting to API endpoints
   - Sanitize user inputs

### Example Production Embedding

```html
<!-- Production widget embedding -->
<link rel="stylesheet" href="https://cdn.yoursite.com/widget.min.css?v=1.0.0">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdn.yoursite.com/widget.min.js?v=1.0.0"></script>

<!-- Widget HTML structure -->
<div id="ragchat-widget-root"></div>

<script>
// Initialize widget
RagChatWidget.configure({
    apiUrl: 'https://api.yoursite.com/api',
    theme: 'light',
    autoOpen: false
});
</script>
```

## Browser Support

- Chrome/Edge: ✅ Latest 2 versions
- Firefox: ✅ Latest 2 versions
- Safari: ✅ Latest 2 versions
- Mobile Browsers: ✅ iOS Safari, Chrome Mobile

## Troubleshooting

### Widget doesn't appear
- Check console for JavaScript errors
- Verify CSS and JS files are loading
- Ensure backend server is running

### API calls fail
- Check API_URL in widget.js
- Verify CORS is configured correctly
- Check network tab for error details

### Styles don't apply
- Check for CSS conflicts with parent page
- Verify CSS file path is correct
- Try adding `!important` to critical styles (use sparingly)

### Widget doesn't close on mobile
- Ensure ESC key handler is working
- Verify close button event listener
- Check z-index conflicts

## Future Enhancements

Planned features:
- [ ] Sound notifications for new messages
- [ ] Minimize state (collapse to small bar)
- [ ] Multi-language support
- [ ] Custom avatars and branding
- [ ] Analytics tracking
- [ ] Typing indicators
- [ ] File upload support
- [ ] Voice input

## Support

For issues or questions:
- Check [CLAUDE.md](../CLAUDE.md) for project documentation
- Review backend API documentation at http://localhost:8000/docs
- Check browser console for error messages

## License

Part of the Yuanyuan Li Profile RAG Chatbot project.
