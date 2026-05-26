// Gathering variables
const userInput = document.getElementById('user-input')
const send = document.getElementById('sendbutton')
const body = document.getElementById('chat-body')

// Function to create bubbles
function appendMessage(text,sender){
    // Create invisbile box
    const bubble = document.createElement('div')

    // attach the respective base and styling of bubble depending the sender(user OR bot)
    bubble.classList.add('message',sender)
    bubble.textContent = text

    //Inject in HTML
    body.appendChild(bubble)

    //auto-scroll to bottom
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
    // Place holder URL since backend is not completed
    const url = "https: url?";
    try{
        // shoot data across internet
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