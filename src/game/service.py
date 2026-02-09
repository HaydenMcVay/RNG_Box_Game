import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from .models import Item, Tier, PlayerState
from .loot import weighted_choice, pick_item_by_rarity
from .save import save_state, load_state

class GameService:
    def __init__(self, data_dir: Path, save_path: Path):
        self.data_dir = data_dir
        self.save_path = save_path

        self.items: List[Item] = self._load_items(data_dir / "items.json")
        self.tiers: List[Tier] = self._load_tiers(data_dir / "tiers.json")
        self.tiers_by_id: Dict[str, Tier] = {t.id: t for t in self.tiers}
        self.items_by_id: Dict[str, Item] = {i.id: i for i in self.items}

        self.state: PlayerState = load_state(save_path)
        self.last_pull: Optional[Item] = None

    def _load_items(self, path: Path) -> List[Item]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [Item(**x) for x in raw]

    def _load_tiers(self, path: Path) -> List[Tier]:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return [Tier(**x) for x in raw]

    def open_box(self, tier_id: str) -> Item:
        tier = self.tiers_by_id[tier_id]
        if self.state.wallet < tier.cost:
            raise ValueError("Not enough money.")
        self.state.wallet -= tier.cost

        rarity = weighted_choice(tier.rarity_weights)
        item = pick_item_by_rarity(self.items, rarity)

        self.state.add_item(item.id, 1)
        self.state.boxes_opened += 1
        self.last_pull = item
        return item

    def sell_item(self, item_id: str, qty: int = 1) -> int:
        item = self.items_by_id[item_id]
        self.state.remove_item(item_id, qty)
        earned = item.sell_value * qty
        self.state.wallet += earned
        return earned

    def save(self) -> None:
        save_state(self.save_path, self.state)

    # A UI-friendly snapshot (so UI doesn’t poke state directly)
    def view(self) -> dict:
        inv_rows = []
        for item_id, qty in sorted(self.state.inventory.items(), key=lambda x: x[0]):
            item = self.items_by_id.get(item_id)
            if item:
                inv_rows.append((item.name, item.rarity, qty, item.sell_value, item.id))
        return {
            "wallet": self.state.wallet,
            "boxes_opened": self.state.boxes_opened,
            "tiers": [(t.id, t.name, t.cost) for t in self.tiers],
            "last_pull": None if not self.last_pull else (self.last_pull.name, self.last_pull.rarity),
            "inventory": inv_rows,
        }
