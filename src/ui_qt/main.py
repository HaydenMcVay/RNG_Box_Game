import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QMessageBox
)

from game.service import GameService

class MainWindow(QWidget):
    def __init__(self, service: GameService):
        super().__init__()
        self.service = service
        self.setWindowTitle("Box Opener Game")

        # Top stats
        self.wallet_label = QLabel()
        self.opened_label = QLabel()
        stats_row = QHBoxLayout()
        stats_row.addWidget(self.wallet_label)
        stats_row.addStretch(1)
        stats_row.addWidget(self.opened_label)

        # Tier picker + open
        self.tier_combo = QComboBox()
        self.open_button = QPushButton("Open Box")
        self.open_button.clicked.connect(self.on_open)

        tier_row = QHBoxLayout()
        tier_row.addWidget(QLabel("Tier:"))
        tier_row.addWidget(self.tier_combo, 1)
        tier_row.addWidget(self.open_button)

        # Last pull
        self.last_pull_label = QLabel("Last pull: (none)")
        self.last_pull_label.setAlignment(Qt.AlignCenter)

        # Inventory list
        self.inv_list = QListWidget()

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_save)

        layout = QVBoxLayout()
        layout.addLayout(stats_row)
        layout.addLayout(tier_row)
        layout.addWidget(self.last_pull_label)
        layout.addWidget(QLabel("Inventory:"))
        layout.addWidget(self.inv_list, 1)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        v = self.service.view()

        self.wallet_label.setText(f"Wallet: ${v['wallet']}")
        self.opened_label.setText(f"Boxes opened: {v['boxes_opened']}")

        # Tiers (keep stable)
        self.tier_combo.blockSignals(True)
        current = self.tier_combo.currentData()
        self.tier_combo.clear()
        for tier_id, name, cost in v["tiers"]:
            self.tier_combo.addItem(f"{name} (${cost})", tier_id)
        # restore selection if possible
        if current:
            idx = self.tier_combo.findData(current)
            if idx >= 0:
                self.tier_combo.setCurrentIndex(idx)
        self.tier_combo.blockSignals(False)

        # Last pull
        if v["last_pull"] is None:
            self.last_pull_label.setText("Last pull: (none)")
        else:
            name, rarity = v["last_pull"]
            self.last_pull_label.setText(f"Last pull: {name} [{rarity.upper()}]")

        # Inventory
        self.inv_list.clear()
        for name, rarity, qty, sell_value, item_id in v["inventory"]:
            text = f"{name} [{rarity}] x{qty}  (sell: {sell_value})"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, item_id)
            self.inv_list.addItem(item)

    def on_open(self):
        tier_id = self.tier_combo.currentData()
        try:
            self.service.open_box(tier_id)
            self.refresh()
        except Exception as e:
            QMessageBox.warning(self, "Can't open", str(e))

    def on_save(self):
        try:
            self.service.save()
            QMessageBox.information(self, "Saved", "Game saved.")
        except Exception as e:
            QMessageBox.warning(self, "Save failed", str(e))

def main():
    root = Path(__file__).resolve().parents[2]  # box_opener/
    data_dir = root / "data"
    save_path = root / "saves" / "save.json"

    service = GameService(data_dir=data_dir, save_path=save_path)

    app = QApplication(sys.argv)
    w = MainWindow(service)
    w.resize(520, 520)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
