// Converts markdown-style formatting to HTML
function parseMarkdown(text) {
    let html = text;
    
    // || или \n -> <br> (перенос строки)
    html = html.replace(/\|\|/g, '<br>');
    html = html.replace(/\/n/g, '<br>');
    
    // **жирный** -> <strong>жирный</strong>
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // *курсив* -> <em>курсив</em>
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    
    
    return html;
}

// Creates a debug window element with title and content
function createDebugWindow(dataTitle, dataContent) {
    const debugWin = document.createElement('div');
    debugWin.className = 'debug_win';
    
    // Create title
    const title = document.createElement('a');
    title.className = 'debug_win_title';
    title.textContent = dataTitle + ' ▼';
    title.style.cursor = 'pointer';
    
    // Create content container
    const content = document.createElement('div');
    content.className = 'debug_win_content';
    
    // If dataContent is a string, create textarea
    if (typeof dataContent === 'string') {
        const textarea = document.createElement('textarea');
        textarea.className = 'debug_win_textarea';
        textarea.value = dataContent;
        content.appendChild(textarea);
    } 
    // If dataContent is an array, process each item
    else if (Array.isArray(dataContent)) {
        dataContent.forEach(item => {
            if (typeof item === 'string') {
                // If item is a string, create textarea
                const textarea = document.createElement('textarea');
                textarea.className = 'debug_win_textarea';
                textarea.value = item;
                content.appendChild(textarea);
            } else if (typeof item === 'object' && item !== null && item.data_title) {
                // If item is an object with data_title, create nested debug window
                const nestedWindow = createDebugWindow(item.data_title, item.data_content);
                content.appendChild(nestedWindow);
            }
        });
    }
    
    // Add click handler for collapsing
    title.addEventListener('click', (e) => {
        e.stopPropagation();
        content.classList.toggle('collapsed');
        if (content.classList.contains('collapsed')) {
            title.textContent = title.textContent.replace('▼', '◀');
        } else {
            title.textContent = title.textContent.replace('◀', '▼');
        }
    });
    
    debugWin.appendChild(title);
    debugWin.appendChild(content);
    
    return debugWin;
}

// Parses server data and creates debug windows
function parseDebugData(dataArray) {
    const debugContainer = document.getElementById('debug');
    
    // Remove old debug windows (keep buttons)
    const oldDebugWins = debugContainer.querySelectorAll('.debug_win');
    oldDebugWins.forEach(win => win.remove());
    
    // Create new debug windows from data
    dataArray.forEach(item => {
        const debugWindow = createDebugWindow(item.data_title, item.data_content);
        debugContainer.appendChild(debugWindow);
    });
}

// ?Extracts data from HTML debug windows and converts to array with addresses
function extractDebugData() {
    const data_to_send = [];
    const debugContainer = document.getElementById('debug');
    
    // Get all top-level debug_win elements
    const topLevelDebugWins = debugContainer.querySelectorAll(':scope > .debug_win');
    
    // Process each top-level debug_win
    topLevelDebugWins.forEach(debugWin => {
        processDebugWin(debugWin, '', data_to_send);
    });
    
    return data_to_send;
}

// Helper function to process a debug_win element recursively
function processDebugWin(debugWin, parentAddress, data_to_send) {
    // Get title from debug_win_title
    const titleElement = debugWin.querySelector(':scope > .debug_win_title');
    if (!titleElement) return;
    
    // Extract title text (remove arrow symbols ▼ or ◀)
    let titleText = titleElement.textContent.replace(/\s*[▼◀]\s*$/, '').trim();
    
    // Build current address
    const curr_address = parentAddress ? `${parentAddress}/${titleText}` : titleText;
    
    // Get debug_win_content
    const contentElement = debugWin.querySelector(':scope > .debug_win_content');
    if (!contentElement) return;
    
    // Get all direct children of content
    const children = contentElement.children;
    let currentEntry = null;
    
    for (let i = 0; i < children.length; i++) {
        const child = children[i];
        
        if (child.classList.contains('debug_win_textarea')) {
            // It's a textarea
            const textareaContent = child.value || '';
            
            if (currentEntry === null) {
                // Create new entry
                currentEntry = {
                    address: curr_address,
                    content: textareaContent
                };
                data_to_send.push(currentEntry);
            } else {
                // Append to existing entry with \n
                currentEntry.content += '\n' + textareaContent;
            }
        } else if (child.classList.contains('debug_win')) {
            // It's a nested debug_win - process recursively
            // Reset currentEntry so next textarea creates new entry
            currentEntry = null;
            processDebugWin(child, curr_address, data_to_send);
        } else {
            // Other element - reset currentEntry
            currentEntry = null;
        }
    }
}

// Displays a message in the chat with nickname, text, and optional profile picture
function addMessage(nickname, messageText, profilePictureUrl = '') {
    const mainDiv = document.getElementById('main');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    
    const profilePic = document.createElement('div');
    profilePic.className = 'profile_picture';
    if (profilePictureUrl) {
        profilePic.style.backgroundImage = `url(${profilePictureUrl})`;
        profilePic.style.backgroundSize = 'cover';
    }
    
    const messagePlace = document.createElement('div');
    messagePlace.className = 'message_place';
    
    const nicknameElement = document.createElement('a');
    nicknameElement.className = 'nickname';
    nicknameElement.textContent = nickname;
    
    const messageTextElement = document.createElement('a');
    messageTextElement.className = 'message_text';
    messageTextElement.innerHTML = parseMarkdown(messageText);
    
    messagePlace.appendChild(nicknameElement);
    messagePlace.appendChild(messageTextElement);
    
    messageDiv.appendChild(profilePic);
    messageDiv.appendChild(messagePlace);
    
    mainDiv.prepend(messageDiv);

    return messageTextElement;
}

function formatting_tosend(action, content) {
    data = { action: action, data: content };
    return(JSON.stringify(data));

}
const sendButton = document.querySelector('.send-button');
const inputField = document.querySelector('.input input[type="text"]');
const receiveDataBtn = document.getElementById('receiveDataBtn');
const sendDataBtn = document.getElementById('sendDataBtn');
var messages_instances = [];

inputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});

// Toggle debug textarea visibility when clicking on title
document.querySelectorAll('.debug_win_title').forEach(title => {
    title.style.cursor = 'pointer';
    // Initialize with down arrow (textarea visible by default)
    title.textContent += ' ▼';
    
    title.addEventListener('click', (e) => {
        e.stopPropagation();

        const content = title.nextElementSibling;
        if (content && content.classList.contains('debug_win_content')) {
                
            // Show textarea
            content.classList.toggle("collapsed");

            if (content.classList.contains('collapsed')) {
            title.textContent = title.textContent.replace('▼', '◀');
            } else {
                title.textContent = title.textContent.replace('◀', '▼');
            }
        }
    });
});





// TODO Curr part to work on
current_character = "Адольф Кристофер"

// TODO Curr part to work on
sendButton.addEventListener('click', () => {
    // text field
    const messageText = inputField.value;

    if (messageText.trim()) {
        console.log(messageText);
        inputField.value = '';
        
        addMessage(current_character + " (YOU)", messageText, "https://i.imgur.com/rv5WneS.jpeg");
        if(!is_writing) {
            // TODO Creating the message on screen
            
            fullText = "";
        }
        sendButton.disabled = true;
        // TODO Sending the message to the server
        sendMessage(messageText, current_character);
        
    }
});





const ws = new WebSocket("ws://localhost:8000/ws")
curr_mes_place = null
let is_writing = false;
let fullText = "";

ws.onmessage = (event) => {
    // Try to parse as JSON (for debug data)
    const jsonData = JSON.parse(event.data);
    if(jsonData.action === "receive_data") {
        parseDebugData(JSON.parse(jsonData.content));
    }
    else if (jsonData.action === "prompt_response_init") {
        data_init = JSON.parse(jsonData.content);
        curr_mes_place = addMessage(data_init.name, "", data_init.picture_url);
        messages_instances[data_init.id] = curr_mes_place;

    } else if(jsonData.action === "prompt_response") {
        
        data_stream = JSON.parse(jsonData.content);

        is_writing = true;
        // disable the button
        sendButton.disabled = true;
        text_chunk = data_stream.message;
        id = data_stream.id;
        curr_mes_place = messages_instances[id];
        console.log(data_stream);
        fullText += text_chunk;
        curr_mes_place.innerHTML = parseMarkdown(fullText);
        if(text_chunk === "[END]") {
            is_writing = false;
            // enable the button
            sendButton.disabled = false;
        } else {
            is_writing = true;
    }

    }
    
    
}


// Sends a message to the server via WebSocket
function sendMessage(message, char_name=current_charcter) {
    const data = {
        "message": message,
        "character": char_name
    };
    ws.send(formatting_tosend('send_message', JSON.stringify(data)));
}

ws.onopen = () => {
    console.log("WebSocket connection established");
}

// Event listener for Receive Data button (placed after WebSocket initialization)
receiveDataBtn.addEventListener('click', () => {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'receive_data' }));
        console.log('Receive Data button clicked!');
    } else {
        console.log('WebSocket is not connected yet. Please wait...');
    }
});

sendDataBtn.addEventListener('click', () => {
    if (ws.readyState === WebSocket.OPEN) {
        const dataToSend = extractDebugData();
        const formattedData = formatting_tosend('send_data', JSON.stringify(dataToSend));
        ws.send(formattedData);
        console.log('Send Data button clicked!');
    } else {
        console.log('WebSocket is not connected yet. Please wait...');
    }
});