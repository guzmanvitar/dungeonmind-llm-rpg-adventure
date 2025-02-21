// Chat response logic //
// Chat typing effect
function typeText(element, text, speed = 75) {
    let i = 0;
    element.innerHTML = ""; // Clear existing text

    let cursor = document.createElement("span");
    cursor.innerHTML = "|";
    cursor.style.animation = "blink 0.8s infinite";
    element.appendChild(cursor);

    function type() {
        if (i < text.length) {
            cursor.remove(); // Remove cursor before adding new text
            element.innerHTML += text[i];
            element.appendChild(cursor); // Append cursor after each letter
            i++;
            scrollToBottom(document.getElementById("chat-log")); // Scroll as text appears
            setTimeout(type, speed);
        } else {
            cursor.remove(); // Remove cursor when typing is finished
        }
    }

    type();
}

let chatHistory = []; // Stores conversation history

// ✅ Load chat history on page load
document.addEventListener("DOMContentLoaded", function () {
    const chatLog = document.getElementById("chat-log");
    let storedChatHistory = sessionStorage.getItem("chatHistory");

    if (!storedChatHistory) {
        // ✅ No history exists, start with the DungeonMind introduction
        let storyText = `Between the realms of thought and reality, I dwell: the DungeonMind,
        the silent watcher, weaving fate into form.
        A thousand souls have walked this path before you, their fates entwined with destiny.
        Now the quill hovers over the page once more—who will you become, traveler?
        A noble warrior, a seeker of knowledge, a trickster in the shadows?
        Or will you forge a path unlike any before?`;

        let messageElement = document.createElement("p");
        messageElement.innerHTML = "<strong>DungeonMind:</strong> ";
        chatLog.appendChild(messageElement);

        typeText(messageElement, storyText);

        // ✅ Store the intro message in history
        chatHistory.push({ role: "assistant", content: storyText });
        sessionStorage.setItem("chatHistory", JSON.stringify(chatHistory));
    } else {
        // ✅ Load existing chat history and display messages
        chatHistory = JSON.parse(storedChatHistory);
        chatHistory.forEach((msg) => {
            if (msg.role !== "system") {
                let messageElement = document.createElement("p");
                messageElement.innerHTML = `<strong>${msg.role === "user" ? "You" : "Dungeon Master"}:</strong> ${msg.content}`;
                chatLog.appendChild(messageElement);
            }
        });
    }

    scrollToBottom();
});


async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const chatLog = document.getElementById("chat-log");

    if (!userInput.trim()) return; // Prevent empty messages

    // ✅ Add user message to chat history
    chatHistory.push({ role: "user", content: userInput });

    // ✅ Display user message in chat log
    chatLog.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    scrollToBottom(chatLog);

    // ✅ Create loading message with animation
    let loadingElement = document.createElement("p");
    loadingElement.innerHTML = `<strong>Dungeon Master:</strong> <span id="loading-text">Thinking</span>`;
    chatLog.appendChild(loadingElement);
    scrollToBottom(chatLog);

    // ✅ Animate ellipsis effect on "Thinking..."
    let dots = 0;
    const loadingInterval = setInterval(() => {
        dots = (dots + 1) % 4;
        document.getElementById("loading-text").innerText = "Thinking" + ".".repeat(dots);
    }, 500);

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_message: userInput,
                conversation_history: chatHistory, // ✅ Send full history
            }),
        });

        if (!response.ok) throw new Error("Failed to fetch response");

        const data = await response.json();

        // ✅ Overwrite chatHistory if API provides a full history
        if (data.conversation_history) {
            chatHistory = data.conversation_history;
        }

        // ✅ First, push metadata into history (but don't display)
        if (data.metadata) {
            data.metadata.forEach((meta) => chatHistory.push(meta));
        }

        // ✅ Then, add assistant's response to chat history
        chatHistory.push({ role: "assistant", content: data.assistant_message });

        // ✅ Remove loading message
        clearInterval(loadingInterval);
        loadingElement.remove();

        // ✅ Only display non-hidden messages
        let messageElement = document.createElement("p");
        messageElement.innerHTML = "<strong>Dungeon Master:</strong> ";
        chatLog.appendChild(messageElement);

        typeText(messageElement, data.assistant_message); // Typing effect
        scrollToBottom(chatLog);

        // ✅ Save updated history in sessionStorage
        sessionStorage.setItem("chatHistory", JSON.stringify(chatHistory));
    } catch (error) {
        console.error("Error:", error);
        clearInterval(loadingInterval);
        chatLog.innerHTML += `<p><strong>Error:</strong> Failed to get response.</p>`;
        scrollToBottom(chatLog);
    }

    // ✅ Clear input field
    document.getElementById("user-input").value = "";
}

// Keep chat log scrolled to the bottom
function scrollToBottom() {
    const chatLog = document.getElementById("chat-log");
    if (chatLog) {
        chatLog.scrollTop = chatLog.scrollHeight;
    }
}

// Allow for key press in user input
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

// Dice roll animation //
function rollDice(sides) {
    let result = Math.floor(Math.random() * sides) + 1;
    let resultElement = document.getElementById("dice-result");

    // Add animation effect
    resultElement.innerText = "🎲 Rolling...";
    setTimeout(() => {
        resultElement.innerText = result;
    }, 500);
}
