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

## Project Structure

```text
box-opener-game/
│
├── main.py              # Application entry point
├── ui/
│   ├── main_window.py   # Main UI components
│   └── assets/          # Images and UI resources
│
├── game/
│   ├── box.py           # Loot box logic
│   ├── item.py          # Item and rarity definitions
│   ├── player.py        # Player inventory and currency
│   └── rng.py           # Randomization utilities
│
├── data/
│   └── items.json       # Item data and drop rates
│
├── requirements.txt
└── README.md
