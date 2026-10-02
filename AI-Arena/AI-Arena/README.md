# AI Arena

A top-down Pygame arena project that evolves from rule-based enemy AI and A* pathfinding into a reinforcement-learning environment.

## Current stage

- Core gameplay implemented
- Enemy combat implemented
- Random maps and collision implemented
- A* navigation implemented
- Vision/FOV and line-of-sight implemented
- Enemy communication implemented
- Search behavior implemented
- Waves, drops, upgrades and shop implemented

## Run

```bash
source .venv/bin/activate
python main.py
```

## Project structure

```text
AI-Arena/
├── game/
│   ├── game.py          # Current integrated game; being split incrementally
│   ├── player.py
│   ├── enemies.py
│   ├── weapons.py
│   ├── projectiles.py
│   ├── map.py
│   ├── waves.py
│   └── items.py
├── ai/
│   ├── vision.py
│   ├── pathfinding.py
│   ├── communication.py
│   └── behavior.py
├── ml/
│   ├── environment.py
│   ├── agent.py
│   ├── train.py
│   └── evaluate.py
├── assets/
├── tests/
├── main.py
└── README.md
```
