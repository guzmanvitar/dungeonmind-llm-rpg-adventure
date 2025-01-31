// Chat response logic
let chatHistory = []; // Stores the conversation history

async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const chatLog = document.getElementById("chat-log");

    if (!userInput.trim()) return;  // Prevent empty messages

    // Add user message to chat history
    chatHistory.push({ role: "user", content: userInput });

    // Display user message in chat log
    chatLog.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    scrollToBottom(chatLog);

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_message: userInput,
                conversation_history: chatHistory, // Send full history
            }),
        });

        if (!response.ok) throw new Error("Failed to fetch response");

        const data = await response.json();

        // Add assistant's response to chat history
        chatHistory.push({ role: "assistant", content: data.assistant_message });

        // Display assistant's response
        chatLog.innerHTML += `<p><strong>Dungeon Master:</strong> ${data.assistant_message}</p>`;
        scrollToBottom(chatLog);
    } catch (error) {
        console.error("Error:", error);
        chatLog.innerHTML += `<p><strong>Error:</strong> Failed to get response.</p>`;
        scrollToBottom(chatLog);
    }

    // Clear input field
    document.getElementById("user-input").value = "";
}

// Keep chat log scrolled to the bottom
function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}

// Allow for key press in user input
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

// Output chat typing effect
function typeText(elementId, text, speed = 50) {
    let i = 0;
    const element = document.getElementById(elementId);
    element.innerHTML = ""; // Clear any existing text

    function type() {
        if (i < text.length) {
            element.innerHTML += text[i];
            i++;
            setTimeout(type, speed); // Adjust speed here (lower = faster)
        }
    }

    type();
}

// Type initial message
document.addEventListener("DOMContentLoaded", function () {
    const storyText = `Between the realms of thought and reality, I dwell: the DungeonMind, the silent watcher,
        weaving fate into form.
        I have chronicled a thousand worlds, but now, the quill hovers over an empty page...
        Tell me, traveler, where does your story begin? Speak, and let the tale unfold!`;

    typeText("chat-text", storyText);
});


// Dice roll animation
function rollDice(sides) {
    let result = Math.floor(Math.random() * sides) + 1;
    let resultElement = document.getElementById("dice-result");

    // Add animation effect
    resultElement.innerText = "🎲 Rolling...";
    setTimeout(() => {
        resultElement.innerText = result;
    }, 500);
}
