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
        document.getElementById("char-ac").textContent = data.armor_class;
        document.getElementById("char-gold").textContent = data.gold.toFixed(2);

        // Populate Traits
        const traitsList = document.getElementById("char-traits");
        traitsList.innerHTML = ""; // Clear previous entries

        if (data.traits && data.traits.length > 0) {
            data.traits.forEach(trait => {
                const listItem = document.createElement("li");
                listItem.textContent = trait;
                traitsList.appendChild(listItem);
            });
        } else {
            traitsList.innerHTML = "<li>No racial traits</li>";
        }

        // Populate Attributes
        const statsList = document.getElementById("char-stats");
        statsList.innerHTML = "";

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
        savingThrowsList.innerHTML = "";

        if (data.saving_throws && data.saving_throws.length > 0) {
            data.saving_throws.forEach(throwStat => {
                const listItem = document.createElement("li");
                listItem.textContent = throwStat;
                savingThrowsList.appendChild(listItem);
            });
        } else {
            savingThrowsList.innerHTML = "<li>No saving throw proficiencies</li>";
        }

        // Populate Proficiencies
        const proficienciesList = document.getElementById("char-proficiencies");
        proficienciesList.innerHTML = "";

        if (data.proficiencies && data.proficiencies.length > 0) {
            data.proficiencies.forEach(prof => {
                const listItem = document.createElement("li");
                listItem.textContent = prof;
                proficienciesList.appendChild(listItem);
            });
        } else {
            proficienciesList.innerHTML = "<li>No proficiencies</li>";
        }

        // Populate Equipment (Inventory)
        const inventoryList = document.getElementById("char-inventory");
        inventoryList.innerHTML = "";

        if (data.inventory && data.inventory.length > 0) {
            data.inventory.forEach(item => {
                const listItem = document.createElement("li");
                listItem.textContent = item;
                inventoryList.appendChild(listItem);
            });
        } else {
            inventoryList.innerHTML = "<li>No equipment</li>";
        }

    } catch (error) {
        console.error("Error loading character sheet:", error);
        document.getElementById("character-info").innerHTML = "<p>Error loading character data.</p>";
    }
});
