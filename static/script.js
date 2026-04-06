document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Scroll to bottom of chat
    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Add a new message to the UI
    function appendMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');
        bubbleDiv.textContent = text;

        messageDiv.appendChild(bubbleDiv);
        chatBox.appendChild(messageDiv);
        scrollToBottom();
    }

    // Add typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message');
        typingDiv.id = 'typing-indicator-wrapper';
        
        const indicator = document.createElement('div');
        indicator.classList.add('typing-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            indicator.appendChild(dot);
        }

        typingDiv.appendChild(indicator);
        chatBox.appendChild(typingDiv);
        scrollToBottom();
    }

    // Remove typing indicator
    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator-wrapper');
        if (indicator) {
            indicator.remove();
        }
    }

    // Handle sending message
    async function sendMessage() {
        const message = userInput.value.trim();
        
        if (message === '') return;

        // 1. Display user message
        appendMessage(message, true);
        userInput.value = '';
        
        // 2. Show "bot is typing..."
        showTypingIndicator();

        try {
            // 3. Send data to Flask backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            // 4. Slight optional delay for realistic feeling
            setTimeout(() => {
                removeTypingIndicator();
                if (response.ok) {
                    appendMessage(data.response, false);
                } else {
                    appendMessage("Oops, I encountered an error.", false);
                }
            }, 600); // 600ms artificial delay

        } catch (error) {
            console.error("Error communicating with backend:", error);
            removeTypingIndicator();
            appendMessage("Sorry, I could not connect to the server.", false);
        }
    }

    // Event listeners
    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Ensure initial scroll position
    scrollToBottom();
});
