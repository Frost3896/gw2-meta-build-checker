import requests
import functools
from build import (
    Skill,
    Trait,
    Specialization,
    Build
)
from equipment import (
    Stats,
    Upgrade,
    Infusion,
    Relic,
    Armor,
    Weapon,
    Accessory,
    Equipment
)


class Api:
    """Interact with the Guild Wars 2 API using an API key."""

    def __init__(self) -> None:
        """Initialize an instance of the Api class."""
        self._api_key = None
        self._clear_cache()

    def _clear_cache(self) -> None:
        """Clear the cache for all decorated methods."""
        self.get_permissions.cache_clear()
        self.get_account_name.cache_clear()
        self.get_characters.cache_clear()

    def _get_endpoint_v2(self, endpoint: str):
        """Perform a GET request to the API and return the JSON response."""
        url = f"https://api.guildwars2.com/v2/{endpoint}"
        headers = {"Authorization": f"Bearer {self._api_key}"}
        return requests.get(url, headers=headers).json()

    def _parse_build_templates(
        self, buildtabs_json
    ) -> list[Build]:
        """Parse build templates from JSON data."""

        # Define empty instances for skill, trait, and specialization.
        EMPTY_SKILL = Skill(
            id=0,
            name=""
        )
        EMPTY_TRAIT = Trait(
            id=0,
            name=""
        )
        EMPTY_SPECIALIZATION = Specialization(
            id=0,
            name="",
            traits=[EMPTY_TRAIT] * 3
        )

        # Initialize an empty list to store build templates.
        build_templates = []

        # Loop through the elements in the JSON data.
        for element in buildtabs_json:
            # Extract keys from the element.
            build_data = element["build"]
            build_name = build_data["name"]
            skills_data = build_data["skills"]
            specializations_data = build_data["specializations"]

            # Skip the build if the name is empty.
            if not build_name:
                continue

            # Initialize an empty list to store skills.
            skills = []

            # Parse skills based on their type.
            for skill_type, skill in skills_data.items():
                if not skill:
                    # Handle the case when a skill is missing.
                    skills.append(
                        EMPTY_SKILL
                    )
                elif isinstance(skill, int):
                    # Handle the case when a skill is an integer.
                    skill_id = skill
                    skills.append(
                        Skill(
                            id=skill_id,
                            name=self.get_skill_name(skill_id)
                        )
                    )
                elif isinstance(skill, list):
                    # Handle the case when skills are provided as a list.
                    for skill_id in skill:
                        if not skill_id:
                            skills.append(
                                EMPTY_SKILL
                            )
                        elif isinstance(skill_id, int):
                            skills.append(
                                Skill(
                                    id=skill_id,
                                    name=self.get_skill_name(skill_id)
                                )
                            )

            # Initialize an empty list to store specializations.
            specializations = []

            # Parse specializations and their associated traits.
            for specialization in specializations_data:
                # Initialize an empty list to store traits.
                traits = []
                if not specialization["id"]:
                    # Handle the case when a specialization is missing.
                    specializations.append(
                        EMPTY_SPECIALIZATION
                    )
                elif isinstance(specialization["id"], int):
                    # Handle the case when a specialization is an integer.
                    for trait_id in specialization["traits"]:
                        if not trait_id:
                            # Handle the case when a trait is missing.
                            traits.append(
                                EMPTY_TRAIT
                            )
                        elif isinstance(trait_id, int):
                            # Handle the case when a trait is an integer.
                            traits.append(
                                Trait(
                                    id=trait_id,
                                    name=self.get_trait_name(trait_id)
                                )
                            )
                    specializations.append(
                        Specialization(
                            id=specialization["id"],
                            name=self.get_specialization_name(
                                specialization["id"]
                            ),
                            traits=traits
                        )
                    )

            # Create a build with a name, skills and specializations.
            build = Build(
                name=build_name,
                skills=skills,
                specializations=specializations
            )

            # Add the build to the list of build templates.
            build_templates.append(build)

        # Return the list of build templates.
        return build_templates

    def _parse_equipment_templates(
        self, equipmenttabs_json
    ) -> list[Equipment]:
        """Parse equipment templates from JSON data."""

        # Define empty instances for stats, upgrade, infusion and relic.
        EMPTY_STATS = Stats(
            id=0,
            name=""
        )
        EMPTY_UPGRADE = Upgrade(
            id=0,
            name=""
        )
        EMPTY_INFUSION = Infusion(
            id=0,
            name=""
        )
        EMPTY_RELIC = Relic(
            id=0,
            name=""
        )

        # Define empty instances for armor, weapon and accessory.
        EMPTY_ARMOR = Armor(
            slot="",
            stats=EMPTY_STATS,
            upgrade=EMPTY_UPGRADE,
            infusion=EMPTY_INFUSION
        )
        EMPTY_WEAPON = Weapon(
            slot="",
            stats=EMPTY_STATS,
            upgrades=[EMPTY_UPGRADE] * 2,
            infusions=[EMPTY_INFUSION] * 2
        )
        EMPTY_ACCESSORY = Accessory(
            slot="",
            stats=EMPTY_STATS,
            infusions=[EMPTY_INFUSION] * 2
        )

        # Define the desired order for armor, weapon, and accessory slots.
        ARMOR_SLOTS = [
            "Helm",
            "Shoulders",
            "Coat",
            "Gloves",
            "Leggings",
            "Boots"
        ]
        WEAPON_SLOTS = [
            "WeaponA1",
            "WeaponA2",
            "WeaponB1",
            "WeaponB2"
        ]
        ACCESSORY_SLOTS = [
            "Backpack",
            "Accessory1",
            "Accessory2",
            "Amulet",
            "Ring1",
            "Ring2",
        ]

        # Initialize an empty list to store equipment templates.
        equipment_templates = []

        # Loop through the elements in the JSON data.
        for element in equipmenttabs_json:
            # Extract keys from the element.
            equipment_data = element["equipment"]
            equipment_name = element["name"]

            # Skip the equipment if the name is empty.
            if not equipment_name:
                continue

            # Skip the equipment if the equipment data is empty.
            if not equipment_data:
                continue

            # Initialize empty lists to store armor, weapons and accessories.
            armor = [EMPTY_ARMOR] * 6
            weapons = [EMPTY_WEAPON] * 4
            accessories =[EMPTY_ACCESSORY] * 6

            # Loop through the items in the equipment data.
            for item in equipment_data:
                # Extract keys from the item.
                if "slot" in item:
                    equipment_slot = item["slot"]
                if "stats" in item:
                    stats_data = item["stats"]
                if "upgrades" in item:
                    upgrades_data = item["upgrades"]
                if "infusions" in item:
                    infusions_data = item["upgrades"]

                if item["slot"] in ARMOR_SLOTS:
                elif item["slot"] in WEAPON_SLOTS:
                elif item["slot"] in ACCESSORY_SLOTS:
                elif item["slot"] == "Relic":
                    relic = EMPTY_RELIC
                    



























    def set_api_key(self, api_key: str) -> None:
        """Set the API key and clear the cache if the key changes."""
        if self._api_key != api_key:
            self._api_key = api_key
            self._clear_cache()

    def check_key(self) -> bool:
        """Check if the API key is valid."""
        tokeninfo = self._get_endpoint_v2("tokeninfo")
        if "text" in tokeninfo:
            return False
        return True

    @functools.lru_cache(maxsize=None)
    def get_permissions(self) -> list[str]:
        """Get the permissions associated with the API key."""
        permissions = self._get_endpoint_v2("tokeninfo")
        return permissions["permissions"]

    @functools.lru_cache(maxsize=None)
    def get_account_name(self) -> str:
        """Get the account name associated with the API key."""
        account_name = self._get_endpoint_v2("account")
        return account_name["name"]

    @functools.lru_cache(maxsize=None)
    def get_characters(self) -> dict[str, str]:
        """Get characters and their profession associated with the API key."""
        character_names = self._get_endpoint_v2("characters")
        profession_names = []
        for character_name in character_names:
            profession_name = self._get_endpoint_v2(
                f"characters/{character_name}/core"
            )
            profession_names.append(profession_name["profession"])
        characters = dict(zip(character_names, profession_names))
        return characters

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
    def get_item_name(self, item_id: int) -> str:
        """Get the name of an item by its ID."""
        item_name = self._get_endpoint_v2(
            f"items/{item_id}"
        )
        return item_name["name"]

    @functools.lru_cache(maxsize=None)
    def get_stats_name(self, stats_id: int) -> str:
        """Get the name of stats by its ID."""
        stats_name = self._get_endpoint_v2(
            f"itemstats/{stats_id}"
        )
        return stats_name["name"]

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
    api.set_api_key("<API_KEY>")
    key_valid = api.check_key()
    if key_valid:
        permissions = api.get_permissions()
        if ("account" in permissions and "characters" in permissions and
                "builds" in permissions and "inventories" in permissions):
            account_name = api.get_account_name()
            characters = api.get_characters()
            print(f"Account name: \n- {account_name}")
            print("API key permissions:")
            for permission in permissions:
                print(f"- {permission.capitalize()}")
            print("Characters:")
            for character_name, profession_name in characters.items():
                print(f"- {character_name} ({profession_name})")
        else:
            print("Insufficient API key permissions.")
    else:
        print("Invalid API key.")
