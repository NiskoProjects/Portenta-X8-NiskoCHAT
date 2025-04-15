/**
 * Chat interface for Portenta X8 LLM
 * Handles user interactions and communication with the backend API
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendButton = document.getElementById('send-button');
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    
    // Chat history for context
    let chatHistory = [];
    
    // Check server health on load
    checkServerHealth();
    
    // Set up event listeners
    chatForm.addEventListener('submit', handleSubmit);
    userInput.addEventListener('keydown', handleKeyDown);
    userInput.addEventListener('input', adjustTextareaHeight);
    
    // Auto-focus the input field
    userInput.focus();
    
    /**
     * Handle form submission
     */
    function handleSubmit(event) {
        event.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input and reset height
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Disable input while waiting for response
        setInputState(false);
        
        // Show thinking indicator
        setStatusThinking();
        
        // Send message to API
        sendMessage(message);
    }
    
    /**
     * Handle keyboard shortcuts
     */
    function handleKeyDown(event) {
        // Submit on Enter (without Shift)
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    }
    
    /**
     * Adjust textarea height based on content
     */
    function adjustTextareaHeight() {
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight) + 'px';
    }
    
    /**
     * Add a message to the chat interface
     */
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Split content by newlines and create paragraphs
        const paragraphs = content.split('\n').filter(line => line.trim() !== '');
        paragraphs.forEach(paragraph => {
            const p = document.createElement('p');
            p.textContent = paragraph;
            messageContent.appendChild(p);
        });
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Add to history if user or assistant message
        if (sender === 'user' || sender === 'assistant') {
            if (sender === 'user') {
                // Start a new pair
                chatHistory.push([content, '']);
            } else if (chatHistory.length > 0) {
                // Complete the current pair
                chatHistory[chatHistory.length - 1][1] = content;
            }
        }
    }
    
    /**
     * Send message to the backend API
     */
    async function sendMessage(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    history: chatHistory.slice(0, -1) // Exclude the current incomplete pair
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Add assistant response to chat
                addMessage(data.response, 'assistant');
            } else {
                // Handle error
                addMessage(`Error: ${data.error || 'Unknown error'}`, 'system');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            addMessage('Sorry, there was an error communicating with the server.', 'system');
            setStatusOffline();
        } finally {
            // Re-enable input
            setInputState(true);
            setStatusOnline();
        }
    }
    
    /**
     * Check server health
     */
    async function checkServerHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (response.ok && data.status === 'healthy') {
                setStatusOnline();
                if (!data.model_loaded) {
                    addMessage('Warning: Model is still loading. Responses may be delayed.', 'system');
                }
            } else {
                setStatusOffline();
                addMessage('Warning: Server is not responding correctly.', 'system');
            }
        } catch (error) {
            console.error('Health check failed:', error);
            setStatusOffline();
        }
    }
    
    /**
     * Set input state (enabled/disabled)
     */
    function setInputState(enabled) {
        userInput.disabled = !enabled;
        sendButton.disabled = !enabled;
        
        if (enabled) {
            userInput.focus();
        }
    }
    
    /**
     * Set status indicator to online
     */
    function setStatusOnline() {
        statusIndicator.className = 'status-indicator online';
        statusText.textContent = 'Connected';
    }
    
    /**
     * Set status indicator to offline
     */
    function setStatusOffline() {
        statusIndicator.className = 'status-indicator offline';
        statusText.textContent = 'Disconnected';
    }
    
    /**
     * Set status indicator to thinking
     */
    function setStatusThinking() {
        statusIndicator.className = 'status-indicator thinking';
        statusText.textContent = 'Thinking';
        statusText.classList.add('thinking-dots');
        
        // Remove thinking dots after response
        const removeDots = () => {
            statusText.classList.remove('thinking-dots');
        };
        
        // Clean up the dots after a timeout or when status changes
        setTimeout(removeDots, 30000);
    }
});
