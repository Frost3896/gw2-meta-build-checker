from dataclasses import dataclass


@dataclass
class Stats:
    """Represent stats with an ID and name."""
    stats_id: int
    stats_name: str


@dataclass
class Upgrade:
    """Represent an upgrade with an ID and name."""
    upgrade_id: int
    upgrade_name: str


@dataclass
class Infusion:
    """Represent an infusion with an ID and name."""
    infusion_id: int
    infusion_name: str


@dataclass
class Relic:
    """Represent a relic with an ID and name."""
    relic_id: int
    relic_name: str


@dataclass
class Armor:
    """Represent an armor piece with a slot, stats, upgrade and infusion."""
    slot: str
    stats: Stats
    upgrade: Upgrade
    infusion: Infusion


@dataclass
class Weapon:
    """Represent a weapon with a slot, stats, upgrades and infusions."""
    slot: str
    stats: Stats
    upgrades: list[Upgrade]
    infusions: list[Infusion]


@dataclass
class Accessory:
    """Represent an accessory with a slot, stats and infusions."""
    slot: str
    stats: Stats
    infusions: list[Infusion]


@dataclass
class Equipment:
    """Represent an equipment with a name, armor, accessories and weapons."""
    equipment_name: str
    armor: list[Armor]
    weapons: list[Weapon]
    accessories: list[Accessory]
    relic: Relic
