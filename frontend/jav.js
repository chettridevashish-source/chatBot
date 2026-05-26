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


//Adding Listener
send.addEventListener('click',function(){
    const message = userInput.value.trim();

    if(!message) return

    // print the users message
    appendMessage(message,'user-message');

    //clear input box
    userInput.value = ''

    // stimulate backend (delay caused by backend)
    setTimeout(function(){
        appendMessage("Brain not biult by backend",'bot-message');
    },1000);
});

