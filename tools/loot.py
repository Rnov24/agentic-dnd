"""
Deterministic 5e Loot & Treasure Generator for Agentic D&D.
Implements official DMG treasure tables for Individual Monsters and Hoards by CR tier.
"""

import json
import random
from pathlib import Path
from typing import Dict, Any, List, Optional
from tools.dice import roll_dice
from tools.compendium import Compendium


class LootGenerator:
    """
    Generates deterministic individual monster loot and dungeon treasure hoards.
    """

    def __init__(self, project_root: Optional[str] = None):
        if project_root:
            self.root = Path(project_root)
        else:
            self.root = Path(__file__).resolve().parent.parent

        self.compendium = Compendium.get_instance(self.root)
        self.treasure_file = self.root / "rules" / "treasure.json"
        self._load_tables()

    def _load_tables(self) -> None:
        if self.treasure_file.exists():
            with open(self.treasure_file, "r", encoding="utf-8") as f:
                self.tables = json.load(f)
        else:
            self.tables = {}

    def _eval_coin_expr(self, expr: str, seed: Optional[int] = None) -> int:
        if not expr:
            return 0
        if "*" in expr:
            dice_part, mult_part = expr.split("*")
            roll_res = roll_dice(dice_part.strip(), seed=seed)
            return roll_res["total"] * int(mult_part.strip())
        else:
            roll_res = roll_dice(expr.strip(), seed=seed)
            return roll_res["total"]

    def generate_individual_treasure(self, cr: float = 1.0, seed: Optional[int] = None) -> Dict[str, Any]:
        """Generates individual monster treasure based on CR."""
        rng = random.Random(seed)
        d100 = rng.randint(1, 100)

        tier_key = "cr_0_4" if cr < 5 else "cr_5_10"
        tier_table = self.tables.get("individual_treasure", {}).get(tier_key, [])

        matched_row = None
        for row in tier_table:
            if row["d100_min"] <= d100 <= row["d100_max"]:
                matched_row = row
                break

        if not matched_row and tier_table:
            matched_row = tier_table[0]

        coins: Dict[str, int] = {}
        total_gp = 0.0

        if matched_row:
            for coin_key in ["cp", "sp", "ep", "gp", "pp"]:
                if coin_key in matched_row:
                    val = self._eval_coin_expr(matched_row[coin_key], seed=rng.randint(1, 1000000))
                    coins[coin_key] = val
                    if coin_key == "cp": total_gp += val * 0.01
                    elif coin_key == "sp": total_gp += val * 0.1
                    elif coin_key == "ep": total_gp += val * 0.5
                    elif coin_key == "gp": total_gp += val * 1.0
                    elif coin_key == "pp": total_gp += val * 10.0

        return {
            "type": "individual_treasure",
            "cr": cr,
            "tier": tier_key,
            "d100_roll": d100,
            "coins": coins,
            "total_value_gp": round(total_gp, 2)
        }

    def generate_hoard_treasure(self, cr: float = 1.0, seed: Optional[int] = None) -> Dict[str, Any]:
        """Generates a full dungeon treasure hoard (coins, gems, art, magic items)."""
        rng = random.Random(seed)
        tier_key = "cr_0_4" if cr < 5 else "cr_5_10"
        hoard_data = self.tables.get("hoard_treasure", {}).get(tier_key, {})

        # 1. Base Coins
        coins: Dict[str, int] = {}
        total_gp = 0.0
        for coin_key, expr in hoard_data.get("coins", {}).items():
            val = self._eval_coin_expr(expr, seed=rng.randint(1, 1000000))
            coins[coin_key] = val
            if coin_key == "cp": total_gp += val * 0.01
            elif coin_key == "sp": total_gp += val * 0.1
            elif coin_key == "ep": total_gp += val * 0.5
            elif coin_key == "gp": total_gp += val * 1.0
            elif coin_key == "pp": total_gp += val * 10.0

        # 2. Gems & Art
        d100_gems = rng.randint(1, 100)
        gems_art_list = []
        for row in hoard_data.get("gems_art", []):
            if row["d100_min"] <= d100_gems <= row["d100_max"]:
                if row.get("type") != "none":
                    count = self._eval_coin_expr(row.get("count", "1d4"), seed=rng.randint(1, 1000000))
                    val_gp = row.get("value_gp", 10)
                    gems_art_list.append({
                        "type": row.get("type"),
                        "count": count,
                        "unit_value_gp": val_gp,
                        "total_gp": count * val_gp,
                        "description": f"{count}x {val_gp} gp {row.get('type')}"
                    })
                    total_gp += count * val_gp
                break

        # 3. Magic Items
        d100_magic = rng.randint(1, 100)
        magic_items_found = []
        for row in hoard_data.get("magic_items", []):
            if row["d100_min"] <= d100_magic <= row["d100_max"]:
                count_expr = row.get("count", 0)
                if count_expr and count_expr != 0:
                    num_items = self._eval_coin_expr(str(count_expr), seed=rng.randint(1, 1000000))
                    rarity = row.get("rarity", "Uncommon")
                    items_dict = self.compendium.get_magic_items()
                    items_list = [v for v in items_dict.values() if isinstance(v, dict)]
                    available = [item for item in items_list if item.get("rarity", "").lower() == rarity.lower()]
                    if not available:
                        available = items_list
                    for _ in range(num_items):
                        if available:
                            chosen = rng.choice(available)
                            magic_items_found.append({
                                "name": chosen.get("name"),
                                "rarity": chosen.get("rarity"),
                                "type": chosen.get("type"),
                                "attunement": chosen.get("attunement", False),
                                "source": chosen.get("_source", "Core 5e Rules")
                            })
                break

        return {
            "type": "hoard_treasure",
            "cr": cr,
            "tier": tier_key,
            "coins": coins,
            "gems_and_art": gems_art_list,
            "magic_items": magic_items_found,
            "total_value_gp": round(total_gp, 2)
        }
