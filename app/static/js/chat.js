document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    loadChatHistory();

    async function loadChatHistory() {
        try {
            const response = await fetch('/api/chat-history');
            const data = await response.json();
            
            if (data.chats) {
                data.chats.forEach(chat => {
                    if (chat.user_message) {
                        appendMessage(chat.user_message, 'user');
                    }
                    if (chat.bot_response) {
                        appendMessage(chat.bot_response, 'bot');
                    }
                });
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
        }
    }

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Send message on Enter (but allow Shift+Enter for new line)
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        appendMessage(message, 'user');
        userInput.value = '';
        userInput.style.height = 'auto';

        // Show typing indicator
        showTypingIndicator();

        try {
            // Create prompt
            const promptResponse = await fetch('/api/prompts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: message })
            });
            
            const promptData = await promptResponse.json();
            
            // Get bot response
            const responseData = await fetch(`/api/prompts/${promptData.prompt_id}/response`);
            const response = await responseData.json();

            // Remove typing indicator and add bot response
            removeTypingIndicator();
            appendMessage(response.response, 'bot');

        } catch (error) {
            removeTypingIndicator();
            appendMessage('Sorry, I encountered an error. Please try again.', 'bot');
        }
    }

    function appendMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message animate__animated animate__fadeIn`;

        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-${sender === 'bot' ? 'robot' : 'user'}"></i>
            </div>
            <div class="message-content">
                <p>${content}</p>
                <span class="timestamp">${timestamp}</span>
            </div>
        `;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'message bot-message typing-indicator animate__animated animate__fadeIn';
        indicator.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <p>Typing<span class="dots">...</span></p>
            </div>
        `;
        chatMessages.appendChild(indicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
});