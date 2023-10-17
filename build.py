from dataclasses import dataclass


@dataclass
class Skill:
    """Represent a skill with a skill ID and skill name."""
    skill_id: int
    skill_name: str


@dataclass
class Trait:
    """Represent a trait with a trait ID and trait name."""
    trait_id: int
    trait_name: str


@dataclass
class Specialization:
    """Represent a specialization with an ID, name, and a list of traits."""
    specialization_id: int
    specialization_name: str
    traits: list[Trait]


@dataclass
class Build:
    """Represent a build with a name, skills, and specializations."""
    build_name: str
    skills: list[Skill]
    specializations: list[Specialization]
