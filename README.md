# Dungeonmind LLM RPG Adventure

## Repo Setup

1. **uv**
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


## Project organization
```
dungeonmind-llm-rpg-adventure/
│
├── frontend/                  # Streamlit or frontend UI components
│   ├── __init__.py
│   ├── app.py                 # Main Streamlit app file
│   ├── components/            # Reusable UI components
│   │   ├── chat.py            # Chat interface
│   │   ├── dice_rolls.py      # Dice roll widget
│   │   └── stats_display.py   # Character stats and inventory display
│   └── assets/                # Static files (e.g., icons, images)
│
├── backend/                   # Backend logic and APIs
│   ├── __init__.py
│   ├── orchestrator.py        # LLM orchestration logic
│   ├── rules_engine.py        # D&D rules validation
│   ├── game_state_manager.py  # Game state handling
│   ├── rag_retriever.py       # Retrieval-augmented generation logic
│   └── models/                # Data models (e.g., for player, NPCs, world)
│       ├── __init__.py
│       ├── player.py
│       ├── npc.py
│       └── game_state.py
│
├── data/                      # Data files and embeddings
│   ├── raw/                   # Raw data for RAG (e.g., D&D rulebooks)
│   ├── processed/             # Processed embeddings for vector search
│   └── saved_games/           # Persistent storage for saved game states
│
├── tests/                     # Unit and integration tests
│   ├── test_frontend.py       # Tests for frontend components
│   ├── test_backend.py        # Tests for backend modules
│   └── test_end_to_end.py     # Full workflow tests
│
├── notebooks/                 # Jupyter notebooks for prototyping
│   └── rag_experiments.ipynb  # Example: testing RAG setup
│
├── docker/                    # Docker configuration
│   ├── Dockerfile             # Dockerfile for containerizing the app
│   ├── docker-compose.yml     # For local multi-container setup (if needed)
│
├── scripts/                   # Utility scripts
│   ├── initialize_db.py       # Script to set up database
│   ├── generate_embeddings.py # Script to process rulebooks into embeddings
│   └── start_server.sh        # Shortcut to start the app
│
├── .env.example               # Example environment variables file
├── requirements.txt           # Python dependencies (or use `pyproject.toml`)
├── README.md                  # Project overview and setup instructions
└── LICENSE                    # License file
```
