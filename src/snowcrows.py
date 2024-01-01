import requests
import functools
from bs4 import (
    BeautifulSoup,
    Tag
)
from constants import (
    EMPTY_ID,
    EMPTY_NAME,
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


class Snowcrows:
    """Interact with snowcrows.com to get Guild Wars 2 build information."""

    def __init__(self) -> None:
        """Initialize an instance of the Snowcrows class."""
        self._BASE_URL = "https://snowcrows.com/builds/"
        self._HEADERS = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
                "Gecko/20100101 Firefox/118.0"
            )
        }
        self._clear_cache()

    def _clear_cache(self) -> None:
        """Clear the cache for all decorated methods."""
        self.get_build_names.cache_clear()
        self.get_build.cache_clear()

    def _get_html_content(self, url: str) -> BeautifulSoup:
        """Request a website and parse it into a BeautifulSoup object."""
        website = requests.get(url, headers=self._HEADERS)
        return BeautifulSoup(website.content, "html.parser")

    def _parse_build(
        self, build_name: str, html_content: BeautifulSoup
    ) -> Build:
        """Parse a build from HTML content."""

        # Initialize empty lists to store skills and specializations.
        skills = []
        specializations = []

        # Create skills and specializations for each slot.
        skills = [Skill.empty()] * 5
        specializations = [Specialization.empty()] * 3

        # Find the HTML tag containing the skills data.
        html_tag = html_content.find(
            "div",
            class_=("bg-neutral-800 "
                    "bg-opacity-20 "
                    "p-4 "
                    "md:p-6 "
                    "rounded-lg "
                    "border "
                    "border-neutral-900 "
                    "mt-0")
        )
        if isinstance(html_tag, Tag):
            html_tag = html_tag.find(
                attrs={"data-armory-ids": True}
            )

        # Extract the skills data from the HTML tag.
        if isinstance(html_tag, Tag) and "data-armory-ids" in html_tag.attrs:
            skills_data = str(html_tag["data-armory-ids"]).split(",")
            for i, skill in enumerate(skills_data):
                skill_id = int(skill)
                skill_name = EMPTY_NAME
                skills[i] = Skill(
                    id=skill_id,
                    name=skill_name
                )

        # Find the HTML tags containing the specializations data.
        html_tags = html_content.find_all(
            "div",
            attrs={"data-armory-ids": True},
            style="display: block !important;"
        )

        # Extract the specializations data from the HTML tags.
        if html_tags:
            for i, html_tag in enumerate(html_tags):
                specializations_data = str(html_tag["data-armory-ids"])
                traits_data = (
                    str(
                        html_tag[f"data-armory-{specializations_data}-traits"]
                    )
                    .split(",")
                )
                specialization_id = int(specializations_data)
                specialization_name = EMPTY_NAME
                traits = [Trait.empty()] * 3
                for j, trait in enumerate(traits_data):
                    trait_id = int(trait)
                    trait_name = EMPTY_NAME
                    traits[j] = Trait(
                        id=trait_id,
                        name=trait_name
                    )
                specializations[i] = Specialization(
                    id=specialization_id,
                    name=specialization_name,
                    traits=traits
                )

        # Create a build with a name and components.
        build = Build(
            name=build_name,
            skills=skills,
            specializations=specializations
        )

        # Return the build.
        return build

    def _parse_equipment(
        self, equipment_name: str, html_content: BeautifulSoup
    ) -> Equipment:
        """Parse an equipment from HTML content."""

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

        # Find the HTML tags containing the equipment data.
        html_tags = html_content.find_all("td")

        # Extract the equipment data from the HTML tags.
        if html_tags:
            equipment_data = html_tags

            # Initialize special item slot indicators.
            slot_indicator = "A"
            main_hand_slot = 1
            off_hand_slot = 1
            ring_slot = 1
            accessory_slot = 1

            # Loop through the equipment data in steps of 2.
            for i in range(0, len(equipment_data), 2):
                # Extract the item data from the equipment data.
                item_data = equipment_data[i].div

                # Extract the item id from the item data.
                item_id = int(item_data["data-armory-ids"])

                # Break the loop if an irrelevant item is found.
                if i > 24 and str(item_data) == (
                        f"<div data-armory-embed=\"items\" "
                        f"data-armory-ids=\"{item_id}\"></div>"
                        ):
                    break

                # Extract the item slot from the equipment data.
                item_slot = str(equipment_data[i + 1].p.span.string)

                # Match the item slot to the slot naming scheme of the API.
                if item_slot == "Main Hand":
                    if main_hand_slot == 1:
                        slot_indicator = "A"
                    else:
                        slot_indicator = "B"
                    item_slot = f"Weapon{slot_indicator}1"
                    main_hand_slot += 1
                if item_slot == "Off Hand":
                    if off_hand_slot == 1 and main_hand_slot == 2:
                        slot_indicator = "A"
                    else:
                        slot_indicator = "B"
                    item_slot = f"Weapon{slot_indicator}2"
                    off_hand_slot += 1
                if item_slot == "Ring":
                    item_slot = f"Ring{ring_slot}"
                    ring_slot += 1
                if item_slot == "Accessory":
                    item_slot = f"Accessory{accessory_slot}"
                    accessory_slot += 1
                if item_slot == "Backpiece":
                    item_slot = "Backpack"

                if item_slot in ARMOR_SLOTS:
                    # Parse armors based on the slot.
                    slot = item_slot
                    if (
                        f"data-armory-{item_id}-stat"
                        not in str(item_data)
                    ):
                        # Handle the case when stats are missing.
                        stats = Stats.empty()
                    else:
                        # Handle the case when stats are available.
                        stats_data = (
                            item_data[f"data-armory-{item_id}-stat"]
                        )
                        stats_id = int(stats_data)
                        stats_name = EMPTY_NAME
                        stats = Stats(
                            id=stats_id,
                            name=stats_name
                        )
                    if (
                        f"data-armory-{item_id}-upgrades"
                        not in str(item_data)
                    ):
                        # Handle the case when upgrades are missing.
                        upgrade = Upgrade.empty()
                    else:
                        # Handle the case when upgrades are available.
                        upgrades_data = (
                            item_data[f"data-armory-{item_id}-upgrades"]
                            .split(",")
                        )
                        upgrade_id = int(upgrades_data[0])
                        upgrade_name = EMPTY_NAME
                        upgrade = Upgrade(
                            id=upgrade_id,
                            name=upgrade_name
                        )
                    # Handle the case when infusions are missing.
                    infusion = Infusion.empty()
                    armors[ARMOR_SLOTS.index(item_slot)] = Armor(
                        slot=slot,
                        stats=stats,
                        upgrade=upgrade,
                        infusion=infusion
                    )

                elif item_slot in WEAPON_SLOTS:
                    # Parse weapons based on the slot.
                    slot = item_slot
                    if not str(html_tags[i + 1].p.contents[0]).split(" ")[1]:
                        # Handle the case when the type is missing.
                        type = EMPTY_TYPE
                    else:
                        # Handle the case when the type is available.
                        type_data = (
                            str(
                                html_tags[i + 1].p.contents[0]
                            )
                            .split(" ")[1]
                        )
                        type = str(type_data)
                    if not str(html_tags[i + 1].p.contents[0]).split(" ")[0]:
                        # Handle the case when stats are missing.
                        stats = Stats.empty()
                    else:
                        # Handle the case when stats are available.
                        stats_data = (
                            str(
                                html_tags[i + 1].p.contents[0]
                            )
                            .split(" ")[0]
                        )
                        stats_id = EMPTY_ID
                        stats_name = str(stats_data)
                        stats = Stats(
                            id=stats_id,
                            name=stats_name
                        )
                    if (
                        f"data-armory-{item_id}-upgrades"
                        not in str(item_data)
                    ):
                        # Handle the case when upgrades are missing.
                        upgrades = [Upgrade.empty()] * 2
                    else:
                        # Handle the case when upgrades are available.
                        upgrades_data = (
                            item_data[f"data-armory-{item_id}-upgrades"]
                            .split(",")
                        )
                        upgrades = []
                        for upgrade in upgrades_data:
                            upgrade_id = int(upgrade)
                            upgrade_name = EMPTY_NAME
                            upgrades.append(
                                Upgrade(
                                    id=upgrade_id,
                                    name=upgrade_name
                                )
                            )
                    # Handle the case when infusions are missing.
                    infusions = [Infusion.empty()] * 2
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
                    if (
                        f"data-armory-{item_id}-stat"
                        not in str(item_data)
                    ):
                        # Handle the case when stats are missing.
                        stats = Stats.empty()
                    else:
                        # Handle the case when stats are available.
                        stats_data = (
                            item_data[f"data-armory-{item_id}-stat"]
                        )
                        stats_id = int(stats_data)
                        stats_name = EMPTY_NAME
                        stats = Stats(
                            id=stats_id,
                            name=stats_name
                        )
                    # Handle the case when infusions are missing.
                    infusions = [Infusion.empty()] * 3
                    accessories[ACCESSORY_SLOTS.index(item_slot)] = Accessory(
                        slot=slot,
                        stats=stats,
                        infusions=infusions
                    )

                elif item_slot == "Relic":
                    # Parse the relic based on the slot.
                    if (
                        "data-armory-ids"
                        not in str(item_data)
                    ):
                        # Handle the case when the relic is missing.
                        relic = Relic.empty()
                    else:
                        # Handle the case when the relic is available.
                        relic_data = item_data["data-armory-ids"]
                        relic_id = int(relic_data)
                        relic_name = EMPTY_NAME
                        relic = Relic(
                            id=relic_id,
                            name=relic_name
                        )

        # Create an equipment with a name and components.
        equipment = Equipment(
            name=equipment_name,
            armors=armors,
            weapons=weapons,
            accessories=accessories,
            relic=relic
        )

        # Return the equipment.
        return equipment

    @functools.lru_cache(maxsize=None)
    def get_build_names(self, profession_name: str) -> list[str]:
        """Get a list of build names for the specified profession name."""

        # Prepare and normalize input data to be used in the URL.
        normalized_profession_name = profession_name.lower()

        # Initialize an empty list to store build names.
        build_names = []

        # Retrieve build names from both "featured" and "beginner" categories.
        for category in ["featured", "beginner"]:
            # Assemble the URL and request the HTML content.
            url = (
                f"{self._BASE_URL}"
                f"{normalized_profession_name}"
                f"?category={category}"
            )
            html_content = self._get_html_content(url)

            # Add non-"Related guides" h2 elements to the list of build names.
            for element in html_content.find_all("h2"):
                if "Related guides" not in element.text:
                    build_names.append(element.text)

        # Strip trailing whitespace from the list of build names.
        for i in range(len(build_names)):
            build_names[i] = build_names[i].rstrip()

        # Return the list of build names.
        return build_names

    @functools.lru_cache(maxsize=None)
    def get_build(
        self, profession_name: str, build_name: str
    ) -> tuple[Build, Equipment]:
        """Get detailed information for a specific build name."""

        # Prepare and normalize input data to be used in the URL.
        normalized_profession_name = profession_name.lower()
        normalized_build_name = build_name.lower().replace(" ", "-")
        normalized_specialization_name = (
            normalized_build_name.rsplit("-", 1)[-1]
        )

        # Assemble the URL and request the HTML content.
        url = (
            f"{self._BASE_URL}"
            f"{normalized_profession_name}/"
            f"{normalized_specialization_name}/"
            f"{normalized_build_name}"
        )
        html_content = self._get_html_content(url)

        # Parse the build and equipment from the HTML content.
        build = self._parse_build(build_name, html_content)
        equipment = self._parse_equipment(build_name, html_content)

        # Return the tuple containing a build and an equipment.
        return build, equipment


if __name__ == "__main__":
    snowcrows = Snowcrows()
    profession_name = "<PROFESSION_NAME>"
    build_names = snowcrows.get_build_names(profession_name)
    print(f"Available builds for {profession_name}:")
    for build_name in build_names:
        print(f"- {build_name}")
