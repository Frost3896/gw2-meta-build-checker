import requests
import functools
from build import Skill, Specialization, Trait, Build
from equipment import Equipment  # more to follow


class Api:
    """Interact with the Guild Wars 2 API using an API key."""

    def __init__(self) -> None:
        """Initialize an instance of the Api class."""
        self._api_key = None
        self._clear_cache()

    def _clear_cache(self) -> None:
        """Clear the cache for all decorated methods."""
        self.check_key.cache_clear()
        self.get_account_name.cache_clear()
        self.get_character_names.cache_clear()
        self.get_profession_name.cache_clear()

    def _get_endpoint_v2(self, endpoint: str):
        """Perform a GET request to the API and return the JSON response."""
        url = f"https://api.guildwars2.com/v2/{endpoint}"
        headers = {"Authorization": f"Bearer {self._api_key}"}
        return requests.get(url, headers=headers).json()

    def _parse_build_templates(
        self, buildtabs_json
    ) -> list[Build]:
        """Parse build templates from JSON data."""
        build_templates = []
        for item in buildtabs_json:
            build_data = item["build"]
            build_name = build_data["name"]
            skills_data = build_data["skills"]
            specializations_data = build_data["specializations"]
            # Skip build if build name is empty
            if not build_name:
                continue
            # Parse skills
            skills = []
            for skill_type, skill in skills_data.items():
                if not skill:
                    skills.append(
                        Skill(
                            skill_id=0,
                            skill_name=""
                        )
                    )
                elif isinstance(skill, int):
                    skill_id = skill
                    skills.append(
                        Skill(
                            skill_id=skill_id,
                            skill_name=self.get_skill_name(skill_id)
                        )
                    )
                elif isinstance(skill, list):
                    for skill_id in skill:
                        if not skill_id:
                            skills.append(
                                Skill(
                                    skill_id=0,
                                    skill_name=""
                                )
                            )
                        elif isinstance(skill_id, int):
                            skills.append(
                                Skill(
                                    skill_id=skill_id,
                                    skill_name=self.get_skill_name(skill_id)
                                )
                            )
            # Parse specializations and traits
            specializations = []
            traits = []
            for specialization in specializations_data:
                if not specialization["id"]:
                    specializations.append(
                        Specialization(
                            specialization_id=0,
                            specialization_name=""
                        )
                    )
                elif isinstance(specialization["id"], int):
                    specializations.append(
                        Specialization(
                            specialization_id=specialization["id"],
                            specialization_name=self.get_specialization_name(
                                specialization["id"]
                            )
                        )
                    )
                for trait_id in specialization["traits"]:
                    if not trait_id:
                        traits.append(
                            Trait(
                                trait_id=0,
                                trait_name=""
                            )
                        )
                    elif isinstance(trait_id, int):
                        traits.append(
                            Trait(
                                trait_id=trait_id,
                                trait_name=self.get_trait_name(trait_id)
                            )
                        )
            # Create a build with name, skills, specializations and traits
            build = Build(
                build_name=build_name,
                skills=skills,
                specializations=specializations,
                traits=traits
            )
            build_templates.append(build)
        return build_templates

    def _parse_equipment_templates(
        self, equipmenttabs_json
    ) -> list[Equipment]:
        """Parse equipment templates from JSON data."""
        equipment_templates = []
        return equipment_templates

    def set_api_key(self, api_key: str) -> None:
        """Set the API key and clear the cache if the key changes."""
        if self._api_key != api_key:
            self._api_key = api_key
            self._clear_cache()

    @functools.lru_cache(maxsize=None)
    def check_key(self) -> bool:
        """Check if the API key is valid and has correct permissions."""
        tokeninfo = self._get_endpoint_v2("tokeninfo")
        if tokeninfo == "Invalid access token":
            return False
        permissions = tokeninfo["permissions"]
        if "account" not in permissions:
            return False
        if "builds" not in permissions:
            return False
        if "characters" not in permissions:
            return False
        if "inventories" not in permissions:
            return False
        return True

    @functools.lru_cache(maxsize=None)
    def get_account_name(self) -> str:
        """Get the account name associated with the API key."""
        account_name = self._get_endpoint_v2("account")
        return account_name["name"]

    @functools.lru_cache(maxsize=None)
    def get_character_names(self) -> list[str]:
        """Get a list of character names associated with the API key."""
        character_names = self._get_endpoint_v2("characters")
        return character_names

    @functools.lru_cache(maxsize=None)
    def get_profession_name(self, character: str) -> str:
        """Get the profession name of a character."""
        profession_name = self._get_endpoint_v2(
            f"characters/{character}/core"
        )
        return profession_name["profession"]

    @functools.lru_cache(maxsize=None)
    def get_skill_name(self, skill_id: int) -> str:
        """Get the name of a skill by its ID."""
        skill_name = self._get_endpoint_v2(
            f"skills/{skill_id}"
        )
        return skill_name["name"]

    @functools.lru_cache(maxsize=None)
    def get_specialization_name(self, specialization_id: int) -> str:
        """Get the name of a specialization by its ID."""
        specialization_name = self._get_endpoint_v2(
            f"specializations/{specialization_id}"
        )
        return specialization_name["name"]

    @functools.lru_cache(maxsize=None)
    def get_trait_name(self, trait_id: int) -> str:
        """Get the name of a trait by its ID."""
        trait_name = self._get_endpoint_v2(
            f"traits/{trait_id}"
        )
        return trait_name["name"]

    @functools.lru_cache(maxsize=None)
    def get_item_stat_name(self, item_stat_id: int) -> str:
        """Get the name of an item stat by its ID."""
        item_stat_name = self._get_endpoint_v2(
            f"itemstats/{item_stat_id}"
        )
        return item_stat_name["name"]

    def get_build_templates(self, character: str) -> list[Build]:
        """Get build templates for a character."""
        buildtabs_json = self._get_endpoint_v2(
            f"characters/{character}/buildtabs?tabs=all"
        )
        build_templates = self._parse_build_templates(
            buildtabs_json
        )
        return build_templates

    def get_equipment_templates(self, character: str) -> list[Equipment]:
        """Get equipment templates for a character."""
        equipmenttabs_json = self._get_endpoint_v2(
            f"characters/{character}/equipmenttabs?tabs=all"
        )
        equipment_templates = self._parse_equipment_templates(
            equipmenttabs_json
        )
        return equipment_templates


if __name__ == "__main__":
    api = Api()
    api_key = api.set_api_key("API-KEY")
    key_valid = api.check_key()
    account_name = api.get_account_name()
    characters = api.get_character_names()
    professions = []
    for character in characters:
        profession = api.get_profession_name(character)
        professions.append(profession)
    print(f"Key valid: {key_valid}")
    print(f"Account name: {account_name}")
    print("Characters:")
    for character, profession in zip(characters, professions):
        print(f"{character} - {profession}")
