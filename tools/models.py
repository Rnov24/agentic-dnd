"""
Typed Domain Models & Schema Contracts for Agentic D&D.
Provides strongly typed dataclass representations, schema validations,
and bidirectional serialization for Characters, Monsters, Magic Items, Spells,
Locations, Encounters, and Mechanics Results.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Tuple, Union


@dataclass
class AbilityScores:
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10

    def get_modifier(self, ability: str) -> int:
        val = getattr(self, ability.lower().strip(), 10)
        return (val - 10) // 2

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AbilityScores':
        if not isinstance(data, dict):
            return cls()
        return cls(
            strength=data.get("strength", data.get("str", 10)),
            dexterity=data.get("dexterity", data.get("dex", 10)),
            constitution=data.get("constitution", data.get("con", 10)),
            intelligence=data.get("intelligence", data.get("int", 10)),
            wisdom=data.get("wisdom", data.get("wis", 10)),
            charisma=data.get("charisma", data.get("cha", 10)),
        )

    def to_dict(self) -> Dict[str, int]:
        return {
            "strength": self.strength,
            "dexterity": self.dexterity,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,
        }


@dataclass
class CharacterModel:
    id: str
    name: str
    species: str = "Human"
    char_class: str = "Fighter"
    level: int = 1
    hp_current: int = 10
    hp_max: int = 10
    ac: int = 10
    stats: AbilityScores = field(default_factory=AbilityScores)
    skills: Dict[str, int] = field(default_factory=dict)
    equipment: List[Union[str, Dict[str, Any]]] = field(default_factory=list)
    attacks: List[Dict[str, Any]] = field(default_factory=list)
    spells_prepared: List[str] = field(default_factory=list)
    spell_slots: Dict[str, Any] = field(default_factory=dict)
    hit_dice_current: int = 1
    hit_dice_max: int = 1
    conditions: List[str] = field(default_factory=list)
    is_player: bool = True
    player_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CharacterModel':
        hp_data = data.get("hp", {})
        if isinstance(hp_data, dict):
            hp_cur = hp_data.get("current", 10)
            hp_m = hp_data.get("max", 10)
        else:
            hp_cur = data.get("hp_current", 10)
            hp_m = data.get("hp_max", 10)

        hd_data = data.get("hit_dice", {})
        if isinstance(hd_data, dict):
            hd_cur = hd_data.get("current", 1)
            hd_m = hd_data.get("max", 1)
        else:
            hd_cur = data.get("hit_dice_current", 1)
            hd_m = data.get("hit_dice_max", 1)

        return cls(
            id=data.get("id", "unknown_char"),
            name=data.get("name", "Unknown Hero"),
            species=data.get("species", data.get("race", "Human")),
            char_class=data.get("class", data.get("char_class", "Fighter")),
            level=data.get("level", 1),
            hp_current=hp_cur,
            hp_max=hp_m,
            ac=data.get("ac", data.get("armor_class", 10)),
            stats=AbilityScores.from_dict(data.get("stats", {})),
            skills=data.get("skills", {}),
            equipment=data.get("equipment", []),
            attacks=data.get("attacks", []),
            spells_prepared=data.get("spells_prepared", []),
            spell_slots=data.get("spell_slots", {}),
            hit_dice_current=hd_cur,
            hit_dice_max=hd_m,
            conditions=data.get("conditions", []),
            is_player=data.get("is_player", True),
            player_name=data.get("player_name"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "class": self.char_class,
            "level": self.level,
            "hp": {
                "current": self.hp_current,
                "max": self.hp_max,
            },
            "ac": self.ac,
            "stats": self.stats.to_dict(),
            "skills": self.skills,
            "equipment": self.equipment,
            "attacks": self.attacks,
            "spells_prepared": self.spells_prepared,
            "spell_slots": self.spell_slots,
            "hit_dice": {
                "current": self.hit_dice_current,
                "max": self.hit_dice_max,
            },
            "conditions": self.conditions,
            "is_player": self.is_player,
            "player_name": self.player_name,
        }


@dataclass
class MonsterModel:
    id: str
    name: str
    size: str = "Medium"
    monster_type: str = "humanoid"
    alignment: str = "neutral"
    ac: int = 10
    hp_current: int = 10
    hp_max: int = 10
    hp_formula: str = ""
    speed: int = 30
    stats: AbilityScores = field(default_factory=AbilityScores)
    skills: Dict[str, int] = field(default_factory=dict)
    cr: str = "1"
    xp: int = 200
    traits: Dict[str, str] = field(default_factory=dict)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    source: str = "Core 5e Rules"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MonsterModel':
        hp_data = data.get("hp", {})
        return cls(
            id=data.get("id", "unknown_monster"),
            name=data.get("name", "Unknown Creature"),
            size=data.get("size", "Medium"),
            monster_type=data.get("type", data.get("monster_type", "humanoid")),
            alignment=data.get("alignment", "neutral"),
            ac=data.get("ac", 10),
            hp_current=hp_data.get("current", 10) if isinstance(hp_data, dict) else 10,
            hp_max=hp_data.get("max", 10) if isinstance(hp_data, dict) else 10,
            hp_formula=hp_data.get("formula", "") if isinstance(hp_data, dict) else "",
            speed=data.get("speed", 30),
            stats=AbilityScores.from_dict(data.get("stats", {})),
            skills=data.get("skills", {}),
            cr=str(data.get("cr", "1")),
            xp=data.get("xp", 200),
            traits=data.get("traits", {}),
            actions=data.get("actions", []),
            source=data.get("_source", data.get("source", "Core 5e Rules")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "type": self.monster_type,
            "alignment": self.alignment,
            "ac": self.ac,
            "hp": {
                "current": self.hp_current,
                "max": self.hp_max,
                "formula": self.hp_formula,
            },
            "speed": self.speed,
            "stats": self.stats.to_dict(),
            "skills": self.skills,
            "cr": self.cr,
            "xp": self.xp,
            "traits": self.traits,
            "actions": self.actions,
            "_source": self.source,
        }


@dataclass
class ItemModel:
    id: str
    name: str
    item_type: str = "Wondrous Item"
    rarity: str = "Common"
    attunement: bool = False
    description: str = ""
    bonuses: Dict[str, Any] = field(default_factory=dict)
    charges: Dict[str, Any] = field(default_factory=dict)
    source: str = "Core 5e Rules"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ItemModel':
        return cls(
            id=data.get("id", "unknown_item"),
            name=data.get("name", "Unknown Item"),
            item_type=data.get("type", "Wondrous Item"),
            rarity=data.get("rarity", "Common"),
            attunement=bool(data.get("attunement", False)),
            description=data.get("description", ""),
            bonuses=data.get("bonuses", {}),
            charges=data.get("charges", {}),
            source=data.get("_source", data.get("source", "Core 5e Rules")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.item_type,
            "rarity": self.rarity,
            "attunement": self.attunement,
            "description": self.description,
            "bonuses": self.bonuses,
            "charges": self.charges,
            "_source": self.source,
        }


@dataclass
class SpellModel:
    id: str
    name: str
    level: int = 0
    school: str = "Evocation"
    casting_time: str = "1 Action"
    spell_range: str = "60 feet"
    components: str = "V, S"
    duration: str = "Instantaneous"
    description: str = ""
    damage: Optional[str] = None
    damage_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpellModel':
        return cls(
            id=data.get("id", "unknown_spell"),
            name=data.get("name", "Unknown Spell"),
            level=data.get("level", 0),
            school=data.get("school", "Evocation"),
            casting_time=data.get("casting_time", "1 Action"),
            spell_range=data.get("range", "60 feet"),
            components=data.get("components", "V, S"),
            duration=data.get("duration", "Instantaneous"),
            description=data.get("description", ""),
            damage=data.get("damage"),
            damage_type=data.get("damage_type"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "school": self.school,
            "casting_time": self.casting_time,
            "range": self.spell_range,
            "components": self.components,
            "duration": self.duration,
            "description": self.description,
            "damage": self.damage,
            "damage_type": self.damage_type,
        }


def validate_character_dict(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validates raw dictionary against Character schema."""
    errors = []
    if not isinstance(data, dict):
        return False, ["Character data must be a dictionary."]
    if not data.get("id"):
        errors.append("Character missing required 'id'.")
    if not data.get("name"):
        errors.append("Character missing required 'name'.")
    return len(errors) == 0, errors
