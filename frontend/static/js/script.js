function rollDice(sides) {
    let result = Math.floor(Math.random() * sides) + 1;
    let resultElement = document.getElementById("dice-result");

    // Add animation effect
    resultElement.innerText = "🎲 Rolling...";
    setTimeout(() => {
        resultElement.innerText = result;
    }, 500);
}
