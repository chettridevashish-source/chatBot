// --- DOM Variables ---
const userInput = document.getElementById('user-input');
const send = document.getElementById('sendbutton');
const body = document.getElementById('chat-body');
const button = document.getElementById('chat-widget');
const cross = document.getElementById('cross');
const container = document.getElementById('chat-container');
const max = document.getElementById('max');

let chatHistory = [];
let isMax = false;

// --- Widget UI Listeners ---
// Open chat widget
button.addEventListener('click', function() {
    container.classList.remove('opacity');
    button.classList.add('opacity');
});

// Maximize/Minimize widget
max.addEventListener('click', function() {
    if (isMax) {
        max.textContent = '❏';
        isMax = false;
    } else {
        max.textContent = '—';
        isMax = true;
    }
    container.classList.toggle("maximize");
});

// Close chat widget
cross.addEventListener('click', function() {
    container.classList.add('opacity');
    button.classList.remove('opacity');
});

// --- Chat UI Functions ---
// Function to create bubbles and avatars
function appendMessage(text, senderType) {
    const row = document.createElement('div');
    row.classList.add('message-row');

    const avatar = document.createElement('div');
    avatar.classList.add('avatar');

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
        row.appendChild(bubble); 
    }

    body.appendChild(row);
    body.scrollTop = body.scrollHeight; // Auto-scroll to bottom
}

// Function to handle sending the message
function sendMessage() {
    const message = userInput.value.trim();
    userInput.value = ''; // Clear input box

    if (!message) return;

    appendMessage(message, 'user-message');

    chatHistory.push({
        role: "user",
        parts: [{text: message}]
    });

    showTypingIndicator();
    botReply(message);
}

// Send button click listener
send.addEventListener('click', function() {
    sendMessage();
});

// Enter key listener
userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

// --- THE API CONNECTION ---
async function botReply(userText) {
    const url = "http://localhost:3000/api/chat";

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json" // CRUCIAL FIX: Tells Node.js we are sending JSON
            },
            body: JSON.stringify({
                message: userText 
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Server Error");
        }

        const data = await response.json();

        removeTypingIndicator();

        appendMessage(data.reply, "bot-message");

        chatHistory.push({
            role: "model",
            parts: [{ text: data.reply }]
        });

    } catch (error) {
        console.error("Connection error:", error);
        removeTypingIndicator();
        appendMessage(
            "Model is not connected. Please check your backend connection.",
            "bot-message"
        );
    }
}

// --- Typing Indicator Logic ---
function showTypingIndicator() {
    const row = document.createElement('div');
    row.classList.add('message-row', 'bot-row');
    row.id = 'typing-row';

    const avatar = document.createElement('div');
    avatar.classList.add('avatar', 'bot-avatar');

    const bubble = document.createElement('div');
    bubble.classList.add('message', 'bot-message', 'typing-indicator');

    // Create 3 bouncing dots
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
    if (typingRow) {
        typingRow.remove();
    }
}

// --- Quick Links Router ---
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('event-btn')) {
        const eventType = event.target.getAttribute('data-event');
        const welcomeBox = document.getElementById('welcome-container');
        if (welcomeBox) welcomeBox.style.display = 'none';

        let routingContext = "";

        if (eventType === 'shop') {
            appendMessage("I want to open a shop or business in Sikkim.", "user-message");
            routingContext = "CONTEXT_ROUTE: USER_WANTS_TO_OPEN_BUSINESS_TRADE_LICENSE";
        } else if (eventType === 'student') {
            appendMessage("I need to apply for student certificates.", "user-message");
            routingContext = "CONTEXT_ROUTE: USER_IS_A_STUDENT_NEEDING_ST_OR_COI";
        } else if (eventType === 'land') {
            appendMessage("I need land or lineage document verification.", "user-message");
            routingContext = "CONTEXT_ROUTE: USER_NEEDS_LAND_LINEAGE_PROOF";
        }

        chatHistory.push({
            role: "user",
            parts: [{ text: routingContext }]
        });

        showTypingIndicator();
        botReply(routingContext);
    }
});