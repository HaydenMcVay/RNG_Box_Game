from __future__ import annotations

import json
from pathlib import Path
from typing import List

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.game.loot import pick_item_by_rarity, weighted_choice
from src.game.models import Item, PlayerState, Tier

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_items(path: Path = DATA_DIR / "items.json") -> List[Item]:
    with path.open("r", encoding="utf-8") as handle:
        raw_items = json.load(handle)
    return [Item(**item) for item in raw_items]


def load_tiers(path: Path = DATA_DIR / "tiers.json") -> List[Tier]:
    with path.open("r", encoding="utf-8") as handle:
        raw_tiers = json.load(handle)
    return [Tier(**tier) for tier in raw_tiers]


class BoxOpenerWindow(QWidget):
    def __init__(self, items: List[Item], tiers: List[Tier]) -> None:
        super().__init__()
        self.items = items
        self.tiers = tiers
        self.state = PlayerState()

        self.setWindowTitle("Box Opener Game")
        self.setMinimumWidth(360)

        self.wallet_label = QLabel()
        self.boxes_label = QLabel()
        self.result_label = QLabel("Open a box to reveal your reward.")

        self.tier_combo = QComboBox()
        for tier in self.tiers:
            self.tier_combo.addItem(f"{tier.name} - {tier.cost} coins", tier.id)

        self.open_button = QPushButton("Open Box")
        self.open_button.clicked.connect(self.open_box)

        self.inventory_list = QListWidget()

        info_layout = QHBoxLayout()
        info_layout.addWidget(self.wallet_label)
        info_layout.addStretch()
        info_layout.addWidget(self.boxes_label)

        layout = QVBoxLayout()
        layout.addLayout(info_layout)
        layout.addWidget(QLabel("Choose a tier:"))
        layout.addWidget(self.tier_combo)
        layout.addWidget(self.open_button)
        layout.addWidget(self.result_label)
        layout.addWidget(QLabel("Inventory"))
        layout.addWidget(self.inventory_list)
        self.setLayout(layout)

        self.refresh_ui()

    def refresh_ui(self) -> None:
        self.wallet_label.setText(f"Wallet: {self.state.wallet} coins")
        self.boxes_label.setText(f"Boxes opened: {self.state.boxes_opened}")
        self.inventory_list.clear()
        for item_id, qty in sorted(self.state.inventory.items()):
            item = next((it for it in self.items if it.id == item_id), None)
            name = item.name if item else item_id
            self.inventory_list.addItem(f"{name} x{qty}")

    def open_box(self) -> None:
        tier = self.tiers[self.tier_combo.currentIndex()]
        if self.state.wallet < tier.cost:
            QMessageBox.information(self, "Not enough coins", "You need more coins to open this box.")
            return

        self.state.wallet -= tier.cost
        rarity = weighted_choice(tier.rarity_weights)
        item = pick_item_by_rarity(self.items, rarity)
        self.state.add_item(item.id)
        self.state.boxes_opened += 1

        self.result_label.setText(f"You received: {item.name} ({item.rarity.title()})")
        self.refresh_ui()


def main() -> None:
    app = QApplication([])
    items = load_items()
    tiers = load_tiers()
    window = BoxOpenerWindow(items, tiers)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
