document.addEventListener("DOMContentLoaded", async function () {
    try {
        const response = await fetch("http://127.0.0.1:8000/character");
        if (!response.ok) throw new Error("Failed to fetch character data");

        const data = await response.json();

        // Populate character information
        document.getElementById("char-name").textContent = data.name;
        document.getElementById("char-race").textContent = data.race;
        document.getElementById("char-class").textContent = data.class;
        document.getElementById("char-background").textContent = data.background;
        document.getElementById("char-hp").textContent = data.current_hit_points;

        // Populate Attributes
        const statsList = document.getElementById("char-stats");
        statsList.innerHTML = ""; // Clear previous entries

        const attributes = [
            { name: "Strength", value: data.strength },
            { name: "Dexterity", value: data.dexterity },
            { name: "Constitution", value: data.constitution },
            { name: "Intelligence", value: data.intelligence },
            { name: "Wisdom", value: data.wisdom },
            { name: "Charisma", value: data.charisma }
        ];

        attributes.forEach(attr => {
            const listItem = document.createElement("li");
            listItem.textContent = `${attr.name}: ${attr.value}`;
            statsList.appendChild(listItem);
        });

        // Populate Saving Throws
        const savingThrowsList = document.getElementById("char-saving-throws");
        savingThrowsList.innerHTML = ""; // Clear previous entries

        if (data.saving_throws && data.saving_throws.length > 0) {
            data.saving_throws.forEach(throwStat => {
                const listItem = document.createElement("li");
                listItem.textContent = throwStat;
                savingThrowsList.appendChild(listItem);
            });
        } else {
            savingThrowsList.innerHTML = "<li>No saving throw proficiencies</li>";
        }

    } catch (error) {
        console.error("Error loading character sheet:", error);
        document.getElementById("character-info").innerHTML = "<p>Error loading character data.</p>";
    }
});
