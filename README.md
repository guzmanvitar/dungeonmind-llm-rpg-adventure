# 🏰 DungeonMind - AI-Powered Dungeon Master

DungeonMind is an AI-driven Dungeon Master assistant designed to guide players through dynamic, immersive, and rule-consistent Dungeons & Dragons (D&D) adventures.
It leverages Large Language Models (LLMs) for inmersive, interactive, and ever-new story telling, enhancing the models with prompt engineering, RAG, and backend rules to enforce D&D mechanics and story consistency.

## 🚀 Features
 - 🧙 AI Dungeon Master: A virtual storyteller that guides players through the adventure.
 - 🎲 D&D Rule Enforcement: Ensures consistency in combat, skill checks, and in-world restrictions.
 - 🔍 Retrieval-Augmented Generation (RAG): Fetches external rulebook details and lore dynamically.
 - 🔀 Multiple LLM Backends: Supports GPT-4, GPT-3.5, and local models.
 - 🖥 Frontend Integration: Flask-based UI with a medieval fantasy aesthetic.
 - 🎛 Configurable Settings: Customize backend models, temperature, and initial prompts.

## 🛠 Tech Stack
| Component     | Technology                |
|--------------|--------------------------|
| **Frontend**  | Flask (HTML, CSS, JavaScript) |
| **Backend**   | FastAPI (Python)         |
| **LLM Service** | OpenAI API (GPT-4, GPT-3.5) |
| **Storage**   | SQLite for game state persistence |
| **Vector Search** | FAISS (retrieval-augmented generation for campaign elements) |
| **Knowledge Graph** | NetworkX (Forgotten Realms world structure) |
| **Web Crawling** | Scrapy + BeautifulSoup (Forgotten Realms Wiki extraction) |


## 🎲 Game Mechanics

### 🏹 Character Creation

The game begins by prompting the player to describe who they are. Based on the player's response, the system parses and assigns a **race**, **class**, and **background** using a natural language model. If the response is ambiguous or incomplete, the system falls back to common default values.

Once the character's basic details are determined, the character sheet is automatically populated using **relational database mappings** that assign appropriate **traits**, **proficiencies**, **starting equipment**, and **abilities** based on:

- **Race:** Determines ability score bonuses, racial traits, and movement speed.
- **Class:** Determines hit die, primary ability, class proficiencies, starting armor, weapons, and spells.
- **Background:** Determines skill proficiencies, starting equipment, and starting gold.

Additionally, the system calculates:
- **Starting Hit Points (HP):** `Hit Die + Constitution Modifier`
- **Armor Class (AC):** Determined by starting armor and Dexterity modifier.
- **Gold & Inventory:** The starting equipment is automatically assigned based on class and background.

📊 **Database ER Diagram**
![DatabaseDiagram](https://github.com/user-attachments/assets/d0a12974-c676-4585-af2e-4a49c38db871)

### 🗺️ Campaign Creation & World Generation
The system dynamically generates Dungeons & Dragons one-shot campaigns set in the Forgotten Realms, ensuring each adventure is immersive, well-structured, and unique. This is achieved using a combination of web crawling, graph-based world modeling, vector search for lore retrieval, and large language models (LLMs) for storytelling.

**🌍 Intelligent Worldbuilding with Web Crawling, Graphs & FAISS**
To create a rich, lore-accurate game world, we implemented:

- 🕷️ Web Crawler (Scrapy + BeautifulSoup) – Extracts structured world data from the Forgotten Realms Wiki, capturing locations, characters, creatures, factions, and history.
- 📖 Knowledge Graph (NetworkX) – Represents Forgotten Realms as an interconnected web of regions, cities, dungeons, and historical events, preserving hierarchical relationships between locations.
- 🧠 FAISS Vector Search – Enables fast retrieval of relevant lore elements (NPCs, monsters, historical events) based on the player’s starting location and campaign theme.
- 📝 Hierarchical Location Selection – Ensures the campaign starts in a specific, lore-rich location, moving from broad continents to detailed cities, settlements, or dungeons.

**🎭 Dynamic Adventure Structure**
The generated campaigns follow a D&D One-Shot Adventure Template, including:

- 🏰 Setting & Worldbuilding – The player begins in a well-defined world with key factions, environmental features, and historical context.
- ⚔️ Core Encounters – A balanced mix of social interactions, exploration challenges, and combat encounters, ensuring a compelling and well-paced adventure.
- 🎲 Narrative Flexibility – Players influence the world through their decisions, with branching paths affecting encounters, rewards, and world reactions.

**📝 Procedural Campaign Generation**
When a campaign is initialized:

- 📍 The system selects an optimal adventure setting based on the user's stated starting point using FAISS similarity search over the extracted Forgotten Realms locations.
- 🔎 Relevant world elements (characters, creatures, items, lore) are retrieved to populate the adventure with meaningful content.
- 🖋️ GPT-4 generates a fully written campaign following the structured one-shot template, seamlessly integrating retrieved lore.
- 📂 The campaign is stored and referenced dynamically to ensure consistency throughout gameplay.


## 📁 Project Structure
```
dungeonmind-llm-rpg-adventure/
│── backend/
│   ├── orchestrator/
│   │   ├── main.py          # FastAPI orchestrator
│   │   ├── models.py        # API request/response models
│   │   ├── services.py      # LLM abstraction layer
│   ├── game_mechanics/
│   │   ├── character_creation.py # Character creation logic
│   ├── constants.py         # Configuration paths
│   ├── config.yaml          # Backend configuration
│── frontend/
│   ├── app.py               # Flask frontend server
│   ├── templates/
│   │   ├── index.html       # Main chat interface
│   │   ├── character.html   # Character sheet UI
│   ├── static/
│   │   ├── css/             # Stylesheets
│   │   ├── js/              # Frontend scripts
│── data/
│   ├── raw/                 # Fetched D&D API data
│── .secrets/
│   ├── open-ai-creds.json   # API credentials (ignored in repo)
│── README.md                # Project documentation
```

## 🔧 Setup & Installation
1️⃣ Clone the Repository
```bash
git clone https://github.com/guzmanvitar/dungeonmind-llm-rpg-adventure.git
cd dungeonmind-llm-rpg-adventure
```
2️⃣ Install Dependencies
This repo uses [uv](https://docs.astral.sh/uv/getting-started/installation) to install and manage dependencies,
as well as to set up the Python environment. After installing `uv` run
```bash
uv python install 3.11.11
uv sync
```
To set up Git hooks for code quality checks run also
```bash
uv run pre-commit install
```
3️⃣ Configure API Credentials
Create a `.secrets/open-ai-creds.json` file and add your OpenAI API key:
```json
{
    "key": "your-openai-api-key-here"
}
```
## 🚀 Running the Project
1️⃣ Start the Backend
```bash
uv run uvicorn src.backend.orchestrator.main:app
```
2️⃣ Start the Frontend
```bash
uv run src/frontend/app.py
```

## 🔮 Roadmap (Upcoming Features)

**Phase 1: Core AI Dungeon Master**

✅ Character creation with race, class, and background

✅ Integrated chat interface with persistent history

**Phase 2: RAG for Game Mechanics & Lore**

✅ Web crawler for Forgotten Realms Wiki to extract world data

✅ Knowledge graph (NetworkX) for structured world representation

✅ FAISS vector search for retrieving world elements dynamically

🔲 Implement ability score retrieval using stored API data

🔲 Fetch relevant D&D rule explanations dynamically

**Phase 3: Interactive Game Elements & AI Dungeon Master Improvements**

✅ Campaign generation using structured templates & AI storytelling

✅ Six-encounter adventure structure for deeper narratives

✅ Implement automated session memory summarization to retain key decisions

🔲 Explicit inventory & spell tracking

🔲 Support dice roll mechanics using AI-driven adjudication

**Phase 4: Multiplayer Co-op Mode**

🔲 Allow multiple players to join the same session

🔲 Implement NPCs and shared game world state


## 🏰 Contributing
Contributions are welcome! Please follow these steps:

1. Fork the Repo
2. Create a Branch (feature/new-mechanic)
3. Commit Your Changes
4. Open a Pull Request
Make sure to follow our code formatting (Black, Flake8) and pre-commit hooks.

## 📜 License
DungeonMind is open-source under the MIT License.

Happy adventuring! 🎲✨
