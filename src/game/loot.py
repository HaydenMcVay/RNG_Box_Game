import random
from typing import Dict, List
from .models import Item

def weighted_choice(weights: Dict[str, int]) -> str:
    total = sum(max(0, w) for w in weights.values())
    if total <= 0:
        raise ValueError("Weights must sum to > 0.")
    r = random.randint(1, total)
    cumulative = 0
    for k, w in weights.items():
        w = max(0, w)
        cumulative += w
        if r <= cumulative:
            return k
    # Fallback (shouldn't happen)
    return next(iter(weights.keys()))

def pick_item_by_rarity(items: List[Item], rarity: str) -> Item:
    pool = [it for it in items if it.rarity == rarity]
    if not pool:
        raise ValueError(f"No items available for rarity '{rarity}'.")
    return random.choice(pool)
