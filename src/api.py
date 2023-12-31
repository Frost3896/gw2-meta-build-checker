import requests
import functools
from constants import (
    EMPTY_TYPE,
    ARMOR_SLOTS,
    WEAPON_SLOTS,
    ACCESSORY_SLOTS
)
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
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "X-Schema-Version": "latest"
        }
        return requests.get(url, headers=headers).json()

    def _parse_build_templates(
        self, buildtabs_json
    ) -> list[Build]:
        """Parse build templates from JSON data."""

        # Initialize an empty list to store build templates.
        build_templates = []

        # Loop through the buildtabs in the JSON data.
        for buildtab in buildtabs_json:
            # Extract keys from the buildtab.
            build_data = buildtab["build"]
            build_name = build_data["name"]
            skills_data = build_data["skills"]
            specializations_data = build_data["specializations"]

            # Skip the build if the name is empty.
            if not build_name:
                continue

            # Initialize empty lists to store skills and specializations.
            skills = []
            specializations = []

            # Parse skills based on their type.
            for skill_type, skill in skills_data.items():
                if not skill:
                    # Handle the case when a skill is missing.
                    skills.append(
                        Skill.empty()
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
                                Skill.empty()
                            )
                        elif isinstance(skill_id, int):
                            skills.append(
                                Skill(
                                    id=skill_id,
                                    name=self.get_skill_name(skill_id)
                                )
                            )

            # Parse specializations and their associated traits.
            for specialization in specializations_data:
                # Initialize an empty list to store traits.
                traits = []
                if not specialization["id"]:
                    # Handle the case when a specialization is missing.
                    specializations.append(
                        Specialization.empty()
                    )
                elif isinstance(specialization["id"], int):
                    # Handle the case when a specialization is an integer.
                    for trait_id in specialization["traits"]:
                        if not trait_id:
                            # Handle the case when a trait is missing.
                            traits.append(
                                Trait.empty()
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

            # Create a build with a name and components.
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

        # Initialize an empty list to store equipment templates.
        equipment_templates = []

        # Loop through the equipmenttabs in the JSON data.
        for equipmenttab in equipmenttabs_json:
            # Extract keys from the equipmenttab.
            equipment_data = equipmenttab["equipment"]
            equipment_name = equipmenttab["name"]

            # Skip the equipment if the name is empty.
            if not equipment_name:
                continue

            # Skip the equipment if the equipment data is empty.
            if not equipment_data:
                continue

            # Initialize empty lists to store armors, weapons and accessories.
            armors = []
            weapons = []
            accessories = []

            # Create armors, weapons and accessories for each slot.
            for slot in ARMOR_SLOTS:
                armor = Armor(
                    slot=slot,
                    stats=Stats.empty(),
                    upgrade=Upgrade.empty(),
                    infusion=Infusion.empty()
                )
                armors.append(armor)
            for slot in WEAPON_SLOTS:
                weapon = Weapon(
                    slot=slot,
                    type=EMPTY_TYPE,
                    stats=Stats.empty(),
                    upgrades=[Upgrade.empty()] * 2,
                    infusions=[Infusion.empty()] * 2
                )
                weapons.append(weapon)
            for slot in ACCESSORY_SLOTS:
                accessory = Accessory(
                    slot=slot,
                    stats=Stats.empty(),
                    infusions=[Infusion.empty()] * 3
                )
                accessories.append(accessory)

            # Create a relic.
            relic = Relic.empty()

            # Loop through the items in the equipment data.
            for item in equipment_data:
                # Extract keys from the item.
                item_id = item["id"]
                item_slot = item["slot"]

                if item_slot in ARMOR_SLOTS:
                    # Parse armors based on the slot.
                    slot = item_slot
                    if "stats" not in item:
                        # Handle the case when stats are missing.
                        stats = Stats.empty()
                    else:
                        # Handle the case when stats are available.
                        stats_data = item["stats"]
                        stats_id = stats_data["id"]
                        stats_name = self.get_stats_name(
                            stats_id
                        )
                        stats = Stats(
                            id=stats_id,
                            name=stats_name
                        )
                    if "upgrades" not in item:
                        # Handle the case when upgrades are missing.
                        upgrade = Upgrade.empty()
                    else:
                        # Handle the case when upgrades are available.
                        upgrades_data = item["upgrades"]
                        upgrade_id = upgrades_data[0]
                        upgrade_name = self.get_item_name(
                            upgrade_id
                        )
                        upgrade = Upgrade(
                            id=upgrade_id,
                            name=upgrade_name
                        )
                    if "infusions" not in item:
                        # Handle the case when infusions are missing.
                        infusion = Infusion.empty()
                    else:
                        # Handle the case when infusions are available.
                        infusions_data = item["infusions"]
                        infusion_id = infusions_data[0]
                        infusion_name = self.get_item_name(
                            infusion_id
                        )
                        infusion = Infusion(
                            id=infusion_id,
                            name=infusion_name
                        )
                    armors[ARMOR_SLOTS.index(item_slot)] = Armor(
                        slot=slot,
                        stats=stats,
                        upgrade=upgrade,
                        infusion=infusion
                    )

                elif item_slot in WEAPON_SLOTS:
                    # Parse weapons based on the slot.
                    slot = item_slot
                    type = self.get_weapon_type(item_id)
                    if "stats" not in item:
                        # Handle the case when stats are missing.
                        stats = Stats.empty()
                    else:
                        # Handle the case when stats are available.
                        stats_data = item["stats"]
                        stats_id = stats_data["id"]
                        stats_name = self.get_stats_name(
                            stats_id
                        )
                        stats = Stats(
                            id=stats_id,
                            name=stats_name
                        )
                    if "upgrades" not in item:
                        # Handle the case when upgrades are missing.
                        upgrades = [Upgrade.empty()] * 2
                    else:
                        # Handle the case when upgrades are available.
                        upgrades_data = item["upgrades"]
                        upgrades = []
                        for upgrade in upgrades_data:
                            upgrade_id = upgrade
                            upgrade_name = self.get_item_name(
                                upgrade_id
                            )
                            upgrades.append(
                                Upgrade(
                                    id=upgrade_id,
                                    name=upgrade_name
                                )
                            )
                    if "infusions" not in item:
                        # Handle the case when infusions are missing.
                        infusions = [Infusion.empty()] * 2
                    else:
                        # Handle the case when infusions are available.
                        infusions_data = item["infusions"]
                        infusions = []
                        for infusion in infusions_data:
                            infusion_id = infusion
                            infusion_name = self.get_item_name(
                                infusion_id
                            )
                            infusions.append(
                                Infusion(
                                    id=infusion_id,
                                    name=infusion_name
                                )
                            )
                    weapons[WEAPON_SLOTS.index(item_slot)] = Weapon(
                        slot=slot,
                        type=type,
                        stats=stats,
                        upgrades=upgrades,
                        infusions=infusions
                    )

                elif item_slot in ACCESSORY_SLOTS:
                    # Parse accessories based on the slot.
                    slot = item_slot
                    if "stats" not in item:
                        # Handle the case when stats are missing.
                        stats = Stats.empty()
                    else:
                        # Handle the case when stats are available.
                        stats_data = item["stats"]
                        stats_id = stats_data["id"]
                        stats_name = self.get_stats_name(
                            stats_id
                        )
                        stats = Stats(
                            id=stats_id,
                            name=stats_name
                        )
                    if "infusions" not in item:
                        # Handle the case when infusions are missing.
                        infusions = [Infusion.empty()] * 3
                    else:
                        # Handle the case when infusions are available.
                        infusions_data = item["infusions"]
                        infusions = []
                        for infusion in infusions_data:
                            infusion_id = infusion
                            infusion_name = self.get_item_name(
                                infusion_id
                            )
                            infusions.append(
                                Infusion(
                                    id=infusion_id,
                                    name=infusion_name
                                )
                            )
                    accessories[ACCESSORY_SLOTS.index(item_slot)] = Accessory(
                        slot=slot,
                        stats=stats,
                        infusions=infusions
                    )

                elif item_slot == "Relic":
                    # Parse the relic based on the slot.
                    relic = Relic.empty()  # Not yet available from the API.

            # Create an equipment with a name and components.
            equipment = Equipment(
                name=equipment_name,
                armors=armors,
                weapons=weapons,
                accessories=accessories,
                relic=relic
            )

            # Add the equipment to the list of equipment templates.
            equipment_templates.append(equipment)

        # Return the list of equipment templates.
        return equipment_templates

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
        permissions_data = self._get_endpoint_v2("tokeninfo")
        permissions = permissions_data["permissions"]
        return permissions

    @functools.lru_cache(maxsize=None)
    def get_account_name(self) -> str:
        """Get the account name associated with the API key."""
        account_data = self._get_endpoint_v2("account")
        account_name = account_data["name"]
        return account_name

    @functools.lru_cache(maxsize=None)
    def get_characters(self) -> dict[str, str]:
        """Get characters and their profession associated with the API key."""
        character_names = self._get_endpoint_v2("characters")
        profession_names = []
        for character_name in character_names:
            character_data = self._get_endpoint_v2(
                f"characters/{character_name}/core"
            )
            profession_name = character_data["profession"]
            profession_names.append(profession_name)
        characters = dict(zip(character_names, profession_names))
        return characters

    @functools.lru_cache(maxsize=None)
    def get_skill_name(self, skill_id: int) -> str:
        """Get the name of a skill by its ID."""
        skill_data = self._get_endpoint_v2(
            f"skills/{skill_id}"
        )
        skill_name = skill_data["name"]
        return skill_name

    @functools.lru_cache(maxsize=None)
    def get_specialization_name(self, specialization_id: int) -> str:
        """Get the name of a specialization by its ID."""
        specialization_data = self._get_endpoint_v2(
            f"specializations/{specialization_id}"
        )
        specialization_name = specialization_data["name"]
        return specialization_name

    @functools.lru_cache(maxsize=None)
    def get_trait_name(self, trait_id: int) -> str:
        """Get the name of a trait by its ID."""
        trait_data = self._get_endpoint_v2(
            f"traits/{trait_id}"
        )
        trait_name = trait_data["name"]
        return trait_name

    @functools.lru_cache(maxsize=None)
    def get_item_data(self, item_id: int):
        """Get the data of an item by its ID."""
        item_data = self._get_endpoint_v2(
            f"items/{item_id}"
        )
        return item_data

    @functools.lru_cache(maxsize=None)
    def get_item_name(self, item_id: int) -> str:
        """Get the name of an item by its ID."""
        item_data = self.get_item_data(item_id)
        item_name = item_data["name"]
        return item_name

    @functools.lru_cache(maxsize=None)
    def get_weapon_type(self, item_id: int) -> str:
        """Get the type of a weapon by its item ID."""
        item_data = self.get_item_data(item_id)
        if item_data["type"] == "Weapon":
            weapon_type_data = item_data["details"]["type"]
            weapon_type = weapon_type_data.lower().capitalize()
        else:
            weapon_type = EMPTY_TYPE
        return weapon_type

    @functools.lru_cache(maxsize=None)
    def get_stats_name(self, stats_id: int) -> str:
        """Get the name of stats by its ID."""
        stats_data = self._get_endpoint_v2(
            f"itemstats/{stats_id}"
        )
        stats_name = stats_data["name"]
        return stats_name

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
