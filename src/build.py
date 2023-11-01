from dataclasses import dataclass


@dataclass
class Skill:
    """Represent a skill with an ID and name."""
    id: int
    name: str


@dataclass
class Trait:
    """Represent a trait with an ID and name."""
    id: int
    name: str


@dataclass
class Specialization:
    """Represent a specialization with an ID, name and traits."""
    id: int
    name: str
    traits: list[Trait]


@dataclass
class Build:
    """Represent a build with a name, skills and specializations."""
    name: str
    skills: list[Skill]
    specializations: list[Specialization]
