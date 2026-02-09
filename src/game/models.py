from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass(frozen=True)
class Item:
    id: str
    name: str
    rarity: str
    sell_value: int

@dataclass(frozen=True)
class Tier:
    id: str
    name: str
    cost: int
    rarity_weights: Dict[str, int]

@dataclass
class PlayerState:
    wallet: int = 100
    inventory: Dict[str, int] = field(default_factory=dict)
    boxes_opened: int = 0

    def add_item(self, item_id: str, qty: int = 1) -> None:
        self.inventory[item_id] = self.inventory.get(item_id, 0) + qty

    def remove_item(self, item_id: str, qty: int = 1) -> None:
        current = self.inventory.get(item_id, 0)
        if qty <= 0 or current < qty:
            raise ValueError("Not enough items to remove.")
        new_qty = current - qty
        if new_qty == 0:
            self.inventory.pop(item_id, None)
        else:
            self.inventory[item_id] = new_qty
