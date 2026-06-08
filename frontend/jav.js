// Gathering variables
const userInput = document.getElementById('user-input')
const send = document.getElementById('sendbutton')
const body = document.getElementById('chat-body')
const button = document.getElementById('chat-widget');
const cross = document.getElementById('cross');
const container = document.getElementById('chat-container');
const max = document.getElementById('max');

let chatHistory = []
let isMax = false;

// for chat to appear on presssing the widget
button.addEventListener('click',function(){
    container.classList.remove('opacity');
    button.classList.add('opacity');
})

//max
max.addEventListener('click',function(){
    if(isMax){
        max.textContent = '❏';
        isMax = false;
    }
    else{
        max.textContent = '—';
        isMax = true;
    }
    container.classList.toggle("maximize");

})

// For the chat to disappear on pressing X.
cross.addEventListener('click',function(){
    container.classList.add('opacity');
    button.classList.remove('opacity');
})

// // Function to create bubbles
// function appendMessage(text,sender){
//     // Create invisbile box
//     const bubble = document.createElement('div')

//     // attach the respective base and styling of bubble depending the sender(user OR bot)
//     bubble.classList.add('message',sender)
//     bubble.textContent = text

//     //Inject in HTML
//     body.appendChild(bubble)

//     //auto-scroll to bottom
//     body.scrollTop = body.scrollHeight;
// }

// Function to create bubbles and avatars
function appendMessage(text, senderType){
    // 1. Create the outer row container
    const row = document.createElement('div');
    row.classList.add('message-row');

    // 2. Create the avatar DIV (Changed from 'img')
    const avatar = document.createElement('div');
    avatar.classList.add('avatar');

    // 3. Create the text bubble
    const bubble = document.createElement('div');
    bubble.classList.add('message');
    bubble.textContent = text;

    // 4. Assemble the pieces based on who is talking
    if (senderType === 'user-message') {
        row.classList.add('user-row');
        bubble.classList.add('user-message');
        
        // Add the User text and color
        // avatar.textContent = 'U';
        // avatar.classList.add('user-avatar');
        
        // Append bubble first, then avatar
        row.appendChild(bubble); 
        // row.appendChild(avatar); 
    } else {
        row.classList.add('bot-row');
        bubble.classList.add('bot-message');
        
        // Add Chad's text and color
        // avatar.textContent = 'AI';
        // avatar.classList.add('bot-avatar');
        
        // Append avatar first, then bubble
        // row.appendChild(avatar); 
        row.appendChild(bubble); 
    }

    // 5. Inject the fully assembled row into the HTML
    body.appendChild(row);

    // auto-scroll to bottom
    body.scrollTop = body.scrollHeight;
}


function sendMessage(){
    const message = userInput.value.trim();
    // We use userInput.value and not.textContetn as textContent is used add text between the elemnts, so when u use it it adds <div> here </div>. But since, input doesnt  have closing tag, it doesnt work in it.

    //clear input box
    userInput.value = '';

    if(!message) return

    // print the users message
    appendMessage(message,'user-message');

    chatHistory.push({
        role : "user",
        parts : [{text:message}]
    })

    showTypingIndicator();
    botReply();
}

// Listener for send button
send.addEventListener('click',function(){
    sendMessage();
});

//Listener for Enter in Input box
userInput.addEventListener('keydown',function(event){
    if(event.key == 'Enter' && !event.shiftKey){
        event.preventDefault();
        sendMessage();
    }
})

// THE API PART

async function botReply(userText){
    
    const url = "http://localhost:3000/chat";
    try{
    
        const response = await fetch(url,{
            method:'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Turning text into for,at the server can read
            body:JSON.stringify({history:chatHistory})
        });

        // security check : If the server actually responded
        if(!response.ok){
            throw new Error('Server Disconnected');
        }

        //Unwrap the server's response
        const data = await response.json();

        removeTypingIndicator();

        // Injecting AI's response into the chat
        appendMessage(data.reply,'bot-message');                

        chatHistory.push({// gemini api does not understand bot or message, the syntax must be strictly "model" and "text"
            role:"model", 
            parts:[{text:data.reply}]
        })
    }
    catch(error){
        console.error('Connection error',error)

        removeTypingIndicator();

        appendMessage('Model is not connected. Please Wait. The backend needs to be connected. Writing more lines to see how it looks on the screen','bot-message');
    }
}




// --- NEW: Typing Indicator Logic ---
function showTypingIndicator() {
    // 1. Create the row and avatar just like a normal bot message
    const row = document.createElement('div');
    row.classList.add('message-row', 'bot-row');
    row.id = 'typing-row'; // Give it a specific ID so we can hunt it down later

    const avatar = document.createElement('div');
    avatar.classList.add('avatar', 'bot-avatar');

    // 2. Create the bubble, but instead of text, add the typing dots
    const bubble = document.createElement('div');
    bubble.classList.add('message', 'bot-message', 'typing-indicator');

    // Create 3 dots
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.classList.add('typing-dot');
        bubble.appendChild(dot);
    }

    // 3. Assemble and inject
    row.appendChild(avatar);
    row.appendChild(bubble);
    body.appendChild(row);
    
    body.scrollTop = body.scrollHeight; // Scroll to see it
}

function removeTypingIndicator() {
    const typingRow = document.getElementById('typing-row');
    if (typingRow) {
        typingRow.remove(); // Destroys the element completely
    }
}
// -----------------------------------




// event manager
// --- Life Event Manager Router ---
// document.addEventListener('click', function(event) {
//     // Check if the clicked element is one of our event buttons
//     if (event.target.classList.contains('event-btn')) {
//         const eventType = event.target.getAttribute('data-event');
        
//         // Hide the welcome selection area cleanly
//         const welcomeBox = document.getElementById('welcome-container');
//         if (welcomeBox) welcomeBox.style.display = 'none';

//         // Route the explicit intents securely
//         if (eventType === 'shop') {
//             appendMessage("🏬 I want to open a shop / business in Sikkim.", "user-message");
//             showTypingIndicator();
//             // Send the hard-coded context instruction straight to the backend
//             botReply("CONTEXT_ROUTE: USER_WANTS_TO_OPEN_BUSINESS_TRADE_LICENSE");
//         } 
//         else if (eventType === 'student') {
//             appendMessage("🎓 I need to apply for student certificates.", "user-message");
//             showTypingIndicator();
//             botReply("CONTEXT_ROUTE: USER_IS_A_STUDENT_NEEDING_ST_OR_COI");
//         } 
//         else if (eventType === 'land') {
//             appendMessage("🏔️ I need land or lineage document verification.", "user-message");
//             showTypingIndicator();
//             botReply("CONTEXT_ROUTE: USER_NEEDS_LAND_LINEAGE_PROOF");
//         }
//     }
// });

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('event-btn')) {
        const eventType = event.target.getAttribute('data-event');
        const welcomeBox = document.getElementById('welcome-container');
        if (welcomeBox) welcomeBox.style.display = 'none';

        let routingContext = "";

        if (eventType === 'shop') {
            appendMessage("🏬 I want to open a shop / business in Sikkim.", "user-message");
            routingContext = "CONTEXT_ROUTE: USER_WANTS_TO_OPEN_BUSINESS_TRADE_LICENSE";
        } else if (eventType === 'student') {
            appendMessage("🎓 I need to apply for student certificates.", "user-message");
            routingContext = "CONTEXT_ROUTE: USER_IS_A_STUDENT_NEEDING_ST_OR_COI";
        } else if (eventType === 'land') {
            appendMessage("🏔️ I need land or lineage document verification.", "user-message");
            routingContext = "CONTEXT_ROUTE: USER_NEEDS_LAND_LINEAGE_PROOF";
        }

        chatHistory.push({
            role: "user",
            parts: [{ text: routingContext }]
        });

        showTypingIndicator();
        botReply();
    }
});