from dataclasses import dataclass


@dataclass
class Skill:
    """Represent a skill with an ID and name."""
    skill_id: int
    skill_name: str


@dataclass
class Specialization:
    """Represent a specialization with an ID and name."""
    specialization_id: int
    specialization_name: str


@dataclass
class Trait:
    """Represent a trait with an ID and name."""
    trait_id: int
    trait_name: str


@dataclass
class Build:
    """Represent a build with a name, skills, specializations and traits."""
    build_name: str
    skills: list[Skill]
    specializations: list[Specialization]
    traits: list[Trait]
