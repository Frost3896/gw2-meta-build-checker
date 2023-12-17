from dataclasses import dataclass

# Define an empty ID, name and slot.
EMPTY_ID = 0
EMPTY_NAME = ""
EMPTY_SLOT = ""

# Define the desired order for armor, weapon, and accessory slots.
ARMOR_SLOTS = (
    "Helm",
    "Shoulders",
    "Coat",
    "Gloves",
    "Leggings",
    "Boots"
)
WEAPON_SLOTS = (
    "WeaponA1",
    "WeaponA2",
    "WeaponB1",
    "WeaponB2"
)
ACCESSORY_SLOTS = (
    "Backpack",
    "Accessory1",
    "Accessory2",
    "Amulet",
    "Ring1",
    "Ring2"
)


@dataclass
class Stats:
    """Represent stats with an ID and name."""
    id: int
    name: str

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            id=EMPTY_ID,
            name=EMPTY_NAME
        )


@dataclass
class Upgrade:
    """Represent an upgrade with an ID and name."""
    id: int
    name: str

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            id=EMPTY_ID,
            name=EMPTY_NAME
        )


@dataclass
class Infusion:
    """Represent an infusion with an ID and name."""
    id: int
    name: str

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            id=EMPTY_ID,
            name=EMPTY_NAME
        )


@dataclass
class Relic:
    """Represent a relic with an ID and name."""
    id: int
    name: str

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            id=EMPTY_ID,
            name=EMPTY_NAME
        )


@dataclass
class Armor:
    """Represent an armor with a slot, stats, upgrade and infusion."""
    slot: str
    stats: Stats
    upgrade: Upgrade
    infusion: Infusion

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            slot=EMPTY_SLOT,
            stats=Stats.empty(),
            upgrade=Upgrade.empty(),
            infusion=Infusion.empty()
        )


@dataclass
class Weapon:
    """Represent a weapon with a slot, stats, upgrades and infusions."""
    slot: str
    stats: Stats
    upgrades: list[Upgrade]
    infusions: list[Infusion]

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            slot=EMPTY_SLOT,
            stats=Stats.empty(),
            upgrades=[Upgrade.empty()] * 2,
            infusions=[Infusion.empty()] * 2
        )


@dataclass
class Accessory:
    """Represent an accessory with a slot, stats and infusions."""
    slot: str
    stats: Stats
    infusions: list[Infusion]

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            slot=EMPTY_SLOT,
            stats=Stats.empty(),
            infusions=[Infusion.empty()] * 3
        )


@dataclass
class Equipment:
    """Represent an equipment with a name, armors, weapons and accessories."""
    name: str
    armors: list[Armor]
    weapons: list[Weapon]
    accessories: list[Accessory]
    relic: Relic

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            name=EMPTY_NAME,
            armors=[Armor.empty()] * 6,
            weapons=[Weapon.empty()] * 4,
            accessories=[Accessory.empty()] * 6,
            relic=Relic.empty()
        )
