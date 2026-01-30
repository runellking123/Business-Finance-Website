/**
 * Wiley University Business & Finance - AI Chatbot
 * Accessible, interactive chatbot widget powered by Claude
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        apiEndpoint: '/.netlify/functions/chat',
        sessionKey: 'wiley_chatbot_session',
        stateKey: 'wiley_chatbot_state',
        maxMessages: 50,
        quickPrompts: [
            { text: 'Pay my bill', message: 'How do I pay my tuition bill?' },
            { text: 'Office hours', message: 'What are the Business & Finance office hours?' },
            { text: 'Financial aid', message: 'How do I apply for financial aid?' },
            { text: 'IT Help', message: 'How do I contact the IT Help Desk?' }
        ]
    };

    // State
    let state = {
        isOpen: false,
        isLoading: false,
        messages: [],
        sessionId: null
    };

    // DOM Elements
    let elements = {};

    // Initialize chatbot
    function init() {
        createChatbotHTML();
        cacheElements();
        bindEvents();
        loadState();
        restoreUIState();
    }

    // Create chatbot HTML structure
    function createChatbotHTML() {
        const container = document.createElement('div');
        container.className = 'chatbot-container';
        container.innerHTML = `
            <!-- Launcher Button -->
            <button class="chatbot-launcher" aria-label="Open chat assistant" aria-expanded="false" aria-controls="chatbot-panel">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 2C6.48 2 2 6.48 2 12c0 1.54.36 2.98.97 4.29L2 22l5.71-.97C9.02 21.64 10.46 22 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2zm-1 15h2v2h-2v-2zm0-10h2v8h-2V7z"/>
                </svg>
                <span class="notification-badge" aria-hidden="true">1</span>
                <span class="chatbot-sr-only">Chat with Wiley Assistant</span>
            </button>

            <!-- Chat Panel -->
            <div class="chatbot-panel" id="chatbot-panel" role="dialog" aria-labelledby="chatbot-title" aria-describedby="chatbot-desc" aria-modal="true">
                <!-- Header -->
                <header class="chatbot-header">
                    <div class="chatbot-header-info">
                        <div class="chatbot-avatar" aria-hidden="true">
                            <svg viewBox="0 0 24 24">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                            </svg>
                        </div>
                        <div class="chatbot-header-text">
                            <h3 id="chatbot-title">Wiley Assistant</h3>
                            <p id="chatbot-desc">Business & Finance Help</p>
                        </div>
                    </div>
                    <div class="chatbot-header-actions">
                        <button class="chatbot-header-btn" id="chatbot-clear" aria-label="Clear conversation" title="Clear conversation">
                            <svg viewBox="0 0 24 24">
                                <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                            </svg>
                        </button>
                        <button class="chatbot-header-btn" id="chatbot-close" aria-label="Close chat">
                            <svg viewBox="0 0 24 24">
                                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                            </svg>
                        </button>
                    </div>
                </header>

                <!-- Messages Area -->
                <div class="chatbot-messages" id="chatbot-messages" role="log" aria-live="polite" aria-label="Chat messages">
                    <div class="chatbot-welcome">
                        <h4>Welcome to Wiley Assistant!</h4>
                        <p>I can help you with questions about Business & Finance services, forms, policies, and more.</p>
                    </div>
                </div>

                <!-- Quick Prompts -->
                <div class="chatbot-quick-prompts" id="chatbot-quick-prompts" role="group" aria-label="Quick questions">
                    ${CONFIG.quickPrompts.map((p, i) => `
                        <button class="chatbot-quick-prompt" data-message="${escapeHtml(p.message)}" tabindex="0">
                            ${escapeHtml(p.text)}
                        </button>
                    `).join('')}
                </div>

                <!-- Input Area -->
                <div class="chatbot-input-area">
                    <div class="chatbot-input-wrapper">
                        <label for="chatbot-input" class="chatbot-sr-only">Type your message</label>
                        <textarea
                            id="chatbot-input"
                            class="chatbot-input"
                            placeholder="Ask me anything..."
                            rows="1"
                            aria-describedby="chatbot-input-hint"
                        ></textarea>
                        <span id="chatbot-input-hint" class="chatbot-sr-only">Press Enter to send, Shift+Enter for new line</span>
                    </div>
                    <button class="chatbot-send-btn" id="chatbot-send" aria-label="Send message" disabled>
                        <svg viewBox="0 0 24 24">
                            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                        </svg>
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(container);
    }

    // Cache DOM elements
    function cacheElements() {
        elements = {
            container: document.querySelector('.chatbot-container'),
            launcher: document.querySelector('.chatbot-launcher'),
            panel: document.querySelector('.chatbot-panel'),
            messages: document.getElementById('chatbot-messages'),
            input: document.getElementById('chatbot-input'),
            sendBtn: document.getElementById('chatbot-send'),
            closeBtn: document.getElementById('chatbot-close'),
            clearBtn: document.getElementById('chatbot-clear'),
            quickPrompts: document.getElementById('chatbot-quick-prompts'),
            badge: document.querySelector('.notification-badge')
        };
    }

    // Bind event listeners
    function bindEvents() {
        // Launcher click
        elements.launcher.addEventListener('click', togglePanel);

        // Close button
        elements.closeBtn.addEventListener('click', closePanel);

        // Clear button
        elements.clearBtn.addEventListener('click', clearConversation);

        // Send button
        elements.sendBtn.addEventListener('click', sendMessage);

        // Input field
        elements.input.addEventListener('input', handleInputChange);
        elements.input.addEventListener('keydown', handleInputKeydown);

        // Quick prompts
        elements.quickPrompts.addEventListener('click', handleQuickPrompt);

        // Keyboard navigation
        document.addEventListener('keydown', handleGlobalKeydown);

        // Click outside to close
        document.addEventListener('click', handleClickOutside);

        // Focus trap
        elements.panel.addEventListener('keydown', handleFocusTrap);
    }

    // Toggle panel open/close
    function togglePanel() {
        if (state.isOpen) {
            closePanel();
        } else {
            openPanel();
        }
    }

    // Open panel
    function openPanel() {
        state.isOpen = true;
        elements.panel.classList.add('open');
        elements.launcher.classList.add('active');
        elements.launcher.setAttribute('aria-expanded', 'true');
        elements.badge.classList.remove('visible');

        // Focus input
        setTimeout(() => {
            elements.input.focus();
        }, 300);

        saveState();
    }

    // Close panel
    function closePanel() {
        state.isOpen = false;
        elements.panel.classList.remove('open');
        elements.launcher.classList.remove('active');
        elements.launcher.setAttribute('aria-expanded', 'false');
        elements.launcher.focus();

        saveState();
    }

    // Handle input change
    function handleInputChange() {
        const hasValue = elements.input.value.trim().length > 0;
        elements.sendBtn.disabled = !hasValue || state.isLoading;

        // Auto-resize textarea
        elements.input.style.height = 'auto';
        elements.input.style.height = Math.min(elements.input.scrollHeight, 100) + 'px';
    }

    // Handle input keydown
    function handleInputKeydown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!elements.sendBtn.disabled) {
                sendMessage();
            }
        }
    }

    // Handle quick prompt click
    function handleQuickPrompt(e) {
        const btn = e.target.closest('.chatbot-quick-prompt');
        if (btn) {
            const message = btn.dataset.message;
            elements.input.value = message;
            handleInputChange();
            sendMessage();
        }
    }

    // Handle global keyboard events
    function handleGlobalKeydown(e) {
        if (e.key === 'Escape' && state.isOpen) {
            closePanel();
        }
    }

    // Handle click outside
    function handleClickOutside(e) {
        if (state.isOpen &&
            !elements.container.contains(e.target)) {
            // Don't close on mobile - too easy to accidentally close
            if (window.innerWidth > 480) {
                closePanel();
            }
        }
    }

    // Focus trap for accessibility
    function handleFocusTrap(e) {
        if (e.key !== 'Tab') return;

        const focusableElements = elements.panel.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
        }
    }

    // Send message
    async function sendMessage() {
        const message = elements.input.value.trim();
        if (!message || state.isLoading) return;

        // Clear input
        elements.input.value = '';
        elements.input.style.height = 'auto';
        elements.sendBtn.disabled = true;

        // Add user message
        addMessage('user', message);

        // Show typing indicator
        state.isLoading = true;
        showTypingIndicator();

        try {
            const response = await fetch(CONFIG.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    messages: state.messages.slice(-10), // Last 10 messages for context
                    currentPage: {
                        url: window.location.pathname,
                        title: document.title
                    },
                    sessionId: state.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Update session ID
            if (data.sessionId) {
                state.sessionId = data.sessionId;
            }

            // Remove typing indicator and add response
            hideTypingIndicator();
            addMessage('assistant', data.response);

        } catch (error) {
            console.error('Chat error:', error);
            hideTypingIndicator();
            showError('Sorry, I encountered an error. Please try again or contact the Business & Finance office directly at (903) 927-3300.');
        } finally {
            state.isLoading = false;
            handleInputChange();
        }
    }

    // Add message to chat
    function addMessage(role, content) {
        const message = {
            role,
            content,
            timestamp: new Date().toISOString()
        };

        state.messages.push(message);

        // Trim old messages
        if (state.messages.length > CONFIG.maxMessages) {
            state.messages = state.messages.slice(-CONFIG.maxMessages);
        }

        renderMessage(message);
        scrollToBottom();
        saveState();

        // Hide quick prompts after first user message
        if (role === 'user' && state.messages.filter(m => m.role === 'user').length === 1) {
            elements.quickPrompts.style.display = 'none';
        }
    }

    // Render a single message
    function renderMessage(message) {
        // Remove welcome message if present
        const welcome = elements.messages.querySelector('.chatbot-welcome');
        if (welcome) {
            welcome.remove();
        }

        const div = document.createElement('div');
        div.className = `chatbot-message ${message.role}`;

        const avatar = message.role === 'assistant' ? 'W' : 'Y';

        div.innerHTML = `
            <div class="chatbot-message-avatar" aria-hidden="true">${avatar}</div>
            <div class="chatbot-message-content">
                ${formatMessage(message.content)}
            </div>
        `;

        elements.messages.appendChild(div);
    }

    // Format message content (handle links, markdown-lite)
    function formatMessage(content) {
        // Escape HTML first
        let formatted = escapeHtml(content);

        // Convert URLs to links
        formatted = formatted.replace(
            /\[([^\]]+)\]\(([^)]+)\)/g,
            '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
        );

        // Convert plain URLs to links
        formatted = formatted.replace(
            /(https?:\/\/[^\s<]+)/g,
            '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
        );

        // Convert **bold** to <strong>
        formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

        // Convert line breaks
        formatted = formatted.replace(/\n/g, '<br>');

        return formatted;
    }

    // Show typing indicator
    function showTypingIndicator() {
        const div = document.createElement('div');
        div.className = 'chatbot-message assistant';
        div.id = 'chatbot-typing';
        div.innerHTML = `
            <div class="chatbot-message-avatar" aria-hidden="true">W</div>
            <div class="chatbot-typing" aria-label="Assistant is typing">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        elements.messages.appendChild(div);
        scrollToBottom();
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        const typing = document.getElementById('chatbot-typing');
        if (typing) {
            typing.remove();
        }
    }

    // Show error message
    function showError(message) {
        const div = document.createElement('div');
        div.className = 'chatbot-error';
        div.setAttribute('role', 'alert');
        div.textContent = message;
        elements.messages.appendChild(div);
        scrollToBottom();
    }

    // Scroll messages to bottom
    function scrollToBottom() {
        elements.messages.scrollTop = elements.messages.scrollHeight;
    }

    // Clear conversation
    function clearConversation() {
        state.messages = [];
        state.sessionId = generateSessionId();

        elements.messages.innerHTML = `
            <div class="chatbot-welcome">
                <h4>Welcome to Wiley Assistant!</h4>
                <p>I can help you with questions about Business & Finance services, forms, policies, and more.</p>
            </div>
        `;

        elements.quickPrompts.style.display = 'flex';
        saveState();

        // Announce to screen readers
        announceToScreenReader('Conversation cleared');
    }

    // Save state to sessionStorage
    function saveState() {
        try {
            sessionStorage.setItem(CONFIG.stateKey, JSON.stringify({
                isOpen: state.isOpen,
                messages: state.messages,
                sessionId: state.sessionId
            }));
        } catch (e) {
            console.warn('Could not save chatbot state:', e);
        }
    }

    // Load state from sessionStorage
    function loadState() {
        try {
            const saved = sessionStorage.getItem(CONFIG.stateKey);
            if (saved) {
                const parsed = JSON.parse(saved);
                state.messages = parsed.messages || [];
                state.sessionId = parsed.sessionId || generateSessionId();
                state.isOpen = parsed.isOpen || false;
            } else {
                state.sessionId = generateSessionId();
            }
        } catch (e) {
            console.warn('Could not load chatbot state:', e);
            state.sessionId = generateSessionId();
        }
    }

    // Restore UI from loaded state
    function restoreUIState() {
        // Render existing messages
        if (state.messages.length > 0) {
            const welcome = elements.messages.querySelector('.chatbot-welcome');
            if (welcome) {
                welcome.remove();
            }

            state.messages.forEach(msg => renderMessage(msg));
            scrollToBottom();

            // Hide quick prompts if there are user messages
            if (state.messages.some(m => m.role === 'user')) {
                elements.quickPrompts.style.display = 'none';
            }
        }

        // Restore open state
        if (state.isOpen) {
            openPanel();
        } else {
            // Show notification badge for new visitors
            if (state.messages.length === 0) {
                setTimeout(() => {
                    elements.badge.classList.add('visible');
                }, 2000);
            }
        }
    }

    // Generate session ID
    function generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Announce to screen readers
    function announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('role', 'status');
        announcement.setAttribute('aria-live', 'polite');
        announcement.className = 'chatbot-sr-only';
        announcement.textContent = message;
        document.body.appendChild(announcement);

        setTimeout(() => {
            announcement.remove();
        }, 1000);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
