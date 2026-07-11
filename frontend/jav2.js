const userInput = document.getElementById('user-input');
const send = document.getElementById('sendbutton');
const body = document.getElementById('chat-body');
const button = document.getElementById('chat-widget');
const cross = document.getElementById('cross');
const container = document.getElementById('chat-container');
const max = document.getElementById('max');

let isMax = false;

button.addEventListener('click', () => {
    container.classList.remove('opacity');
    button.classList.add('opacity');
});

max.addEventListener('click', () => {
    if(isMax) {
        max.innerHTML = '<i class="fa-solid fa-expand"></i>';
        isMax = false;
    } else {
        max.innerHTML = '<i class="fa-solid fa-compress"></i>';
        isMax = true;
    }
    container.classList.toggle("maximize");
});

cross.addEventListener('click', () => {
    container.classList.add('opacity');
    button.classList.remove('opacity');
});

function appendMessage(text, senderType) {
    const row = document.createElement('div');
    row.classList.add('message-row');

    const bubble = document.createElement('div');
    bubble.classList.add('message');
    bubble.textContent = text;

    if (senderType === 'user-message') {
        row.classList.add('user-row');
        bubble.classList.add('user-message');
        row.appendChild(bubble);
    } else {
        row.classList.add('bot-row');
        bubble.classList.add('bot-message');
        const avatar = document.createElement('div');
        avatar.classList.add('avatar', 'bot-avatar');
        avatar.innerHTML = '<i class="fa-solid fa-robot"></i>';
        row.appendChild(avatar);
        row.appendChild(bubble);
    }

    body.appendChild(row);
    body.scrollTop = body.scrollHeight; 
}

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    userInput.value = '';
    userInput.disabled = true;
    send.disabled = true;

    appendMessage(message, 'user-message');
    showTypingIndicator();
    botReply(message);
}

send.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

async function botReply(messageText) {
    const url = "http://localhost:3000/api/chat";
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: messageText })
        });

        if (!response.ok) throw new Error('Server Disconnected');

        const data = await response.json();
        
        removeTypingIndicator();
        appendMessage(data.reply, 'bot-message');

    } catch (error) {
        console.error('Connection error', error);
        removeTypingIndicator();
        appendMessage('Connection lost. Please check if the backend is running.', 'bot-message');
    } finally {
        userInput.disabled = false;
        send.disabled = false;
        userInput.focus();
    }
}

function showTypingIndicator() {
    const row = document.createElement('div');
    row.classList.add('message-row', 'bot-row');
    row.id = 'typing-row';

    const avatar = document.createElement('div');
    avatar.classList.add('avatar', 'bot-avatar');
    avatar.innerHTML = '<i class="fa-solid fa-robot"></i>';

    const bubble = document.createElement('div');
    bubble.classList.add('message', 'bot-message', 'typing-indicator');

    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.classList.add('typing-dot');
        bubble.appendChild(dot);
    }

    row.appendChild(avatar);
    row.appendChild(bubble);
    body.appendChild(row);
    body.scrollTop = body.scrollHeight;
}

function removeTypingIndicator() {
    const typingRow = document.getElementById('typing-row');
    if (typingRow) typingRow.remove();
}

document.addEventListener('click', (event) => {
    if (event.target.classList.contains('event-btn')) {
        const eventType = event.target.getAttribute('data-event');
        const welcomeBox = document.getElementById('welcome-container');
        if (welcomeBox) welcomeBox.style.display = 'none';

        let routingContext = "";
        if (eventType === 'shop') routingContext = "I want to open a shop / business in Sikkim.";
        else if (eventType === 'student') routingContext = "I need to apply for student certificates.";
        else if (eventType === 'land') routingContext = "I need land or lineage document verification.";

        if(routingContext) {
            userInput.disabled = true;
            send.disabled = true;
            appendMessage(routingContext, "user-message");
            showTypingIndicator();
            botReply(routingContext);
        }
    }
});