# Box Opener Game

A desktop loot box / case-opening game built in Python using PySide6.  
The project simulates randomized rewards with rarity tiers and a graphical user interface, designed to be modular and easily extensible.

---

## Overview

The Box Opener Game allows users to open virtual boxes using in-game currency. Each box uses weighted randomization to determine item rarity and rewards, which are then added to the player's inventory. The project separates game logic from the UI to support maintainability and future expansion.

---

## Features

- Randomized loot box system
- Multiple rarity tiers
- Inventory tracking
- In-game currency system
- Graphical user interface using PySide6
- Modular and extensible code structure

---

## Technologies Used

- Python 3.10+
- PySide6 (Qt for Python)

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the App

```bash
python -m src.ui_qt.main
```

## Project Structure

```text
RNG_Box_Game/
│
├── src/
│   ├── ui_qt/
│   │   └── main.py         # Qt UI entry point
│   └── game/
│       ├── loot.py         # Loot roll logic
│       ├── models.py       # Item, tier, and player models
│       ├── save.py         # Save system (placeholder)
│       └── service.py      # Game services (placeholder)
│
├── data/
│   ├── items.json          # Item data and drop rates
│   └── tiers.json          # Tier costs and rarity weights
│
├── requirements.txt
└── README.md
