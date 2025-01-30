function rollDice(sides) {
    let result = Math.floor(Math.random() * sides) + 1;
    let resultElement = document.getElementById("dice-result");

    // Add animation effect
    resultElement.innerText = "🎲 Rolling...";
    setTimeout(() => {
        resultElement.innerText = result;
    }, 500);
}

async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const chatLog = document.getElementById("chat-log");

    if (!userInput.trim()) return;  // Prevent empty messages

    // Add user message to chat log
    chatLog.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    scrollToBottom(chatLog);

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_message: userInput,
                conversation_history: []
            }),
        });

        if (!response.ok) throw new Error("Failed to fetch response");

        const data = await response.json();

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

// Function to keep chat log scrolled to the bottom
function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}

document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
