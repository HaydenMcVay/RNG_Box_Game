import json
from pathlib import Path
from .models import PlayerState

def save_state(path: Path, state: PlayerState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "wallet": state.wallet,
        "inventory": state.inventory,
        "boxes_opened": state.boxes_opened,
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def load_state(path: Path) -> PlayerState:
    if not path.exists():
        return PlayerState()
    data = json.loads(path.read_text(encoding="utf-8"))
    return PlayerState(
        wallet=int(data.get("wallet", 100)),
        inventory=dict(data.get("inventory", {})),
        boxes_opened=int(data.get("boxes_opened", 0)),
    )
