import requests
import functools
from bs4 import (
    BeautifulSoup,
    Tag
)
from build import (
    EMPTY_NAME,
    Skill,
    Trait,
    Specialization,
    Build
)
from equipment import (
    EMPTY_ID,
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
            "div", style="display: block !important;"
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
