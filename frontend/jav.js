// Gathering variables
const userInput = document.getElementById('user-input')
const send = document.getElementById('sendbutton')
const body = document.getElementById('chat-body')
const button = document.getElementById('chat-widget');
const cross = document.getElementById('cross');
const container = document.getElementById('chat-container');

// for chat to appear on presssing the widget
button.addEventListener('click',function(){
    container.classList.remove('opacity');
    button.classList.add('opacity');
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
        avatar.textContent = 'U';
        avatar.classList.add('user-avatar');
        
        // Append bubble first, then avatar
        row.appendChild(bubble); 
        row.appendChild(avatar); 
    } else {
        row.classList.add('bot-row');
        bubble.classList.add('bot-message');
        
        // Add Chad's text and color
        avatar.textContent = 'AI';
        avatar.classList.add('bot-avatar');
        
        // Append avatar first, then bubble
        row.appendChild(avatar); 
        row.appendChild(bubble); 
    }

    // 5. Inject the fully assembled row into the HTML
    body.appendChild(row);

    // auto-scroll to bottom
    body.scrollTop = body.scrollHeight;
}


function sendMessage(){
    const message = userInput.value.trim();

    if(!message) return

    // print the users message
    appendMessage(message,'user-message');

    //clear input box
    userInput.value = ''

    // stimulate backend (delay caused by backend)
        // setTimeout(function(){
        //     appendMessage("Brain not biult by backend",'bot-message');
        // },1000);
    
    // Actual connection directly from API function(Not stimulated).

    botReply(message);
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
    
    const url = "https://embattled-blimp-duchess.ngrok-free.dev/chat";
    try{
    
        const response = await fetch(url,{
            method:'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Turning text into for,at the server can read
            body:JSON.stringify({message:userText})
        });

        // security check : If the server actually responded
        if(!response.ok){
            throw new Error('Server Disconnected');
        }

        //Unwrap the server's response
        const data = await response.json();

        // Injecting AI's response into the chat
        appendMessage(data.reply,'bot-message');
    }
    catch(error){
        console.error('Connection error',error)
        appendMessage('Chad is not completed. Please Wait.','bot-message');
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
    avatar.textContent = 'AI';

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