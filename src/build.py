from dataclasses import dataclass

# Define an empty ID and name.
_EMPTY_ID = 0
_EMPTY_NAME = ""


@dataclass
class Skill:
    """Represent a skill with an ID and name."""
    id: int
    name: str

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            id=_EMPTY_ID,
            name=_EMPTY_NAME
        )


@dataclass
class Trait:
    """Represent a trait with an ID and name."""
    id: int
    name: str

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            id=_EMPTY_ID,
            name=_EMPTY_NAME
        )


@dataclass
class Specialization:
    """Represent a specialization with an ID, name and traits."""
    id: int
    name: str
    traits: list[Trait]

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            id=_EMPTY_ID,
            name=_EMPTY_NAME,
            traits=[Trait.empty()] * 3
        )


@dataclass
class Build:
    """Represent a build with a name, skills and specializations."""
    name: str
    skills: list[Skill]
    specializations: list[Specialization]

    @classmethod
    def empty(cls):
        """Create an instance with empty values."""
        return cls(
            name=_EMPTY_NAME,
            skills=[Skill.empty()] * 5,
            specializations=[Specialization.empty()] * 3
        )
