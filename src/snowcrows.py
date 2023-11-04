import requests
import functools
from bs4 import BeautifulSoup
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

    def _parse_build(self, html_data: BeautifulSoup) -> Build:
        """Parse a build from HTML data."""
        return build

    def _parse_equipment(self, html_data: BeautifulSoup) -> Equipment:
        """Parse an equipment from HTML data."""
        return equipment

    @functools.lru_cache(maxsize=None)
    def get_build_names(self, profession_name: str) -> list[str]:
        """Get a list of build names for the specified profession name."""

        # Prepare and normalize input data to be used in the URL.
        profession_name = profession_name.lower()

        # Initialize an empty list to store build names.
        build_names = []

        # Retrieve build names from both "featured" and "beginner" categories.
        for category in ["featured", "beginner"]:
            # Assemble the URL and request the HTML content.
            url = (
                f"{self._BASE_URL}"
                f"{profession_name}?category={category}"
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
        profession_name = profession_name.lower()
        build_name = build_name.lower().replace(" ", "-")
        specialization_name = build_name.rsplit("-", 1)[-1]

        # Assemble the URL and request the HTML content.
        url = (
            f"{self._BASE_URL}"
            f"{profession_name}/{specialization_name}/{build_name}"
        )
        html_content = self._get_html_content(url)

        # Parse the build and equipment from the HTML data.
        build = self._parse_build(html_content)
        equipment = self._parse_equipment(html_content)

        # Return the tuple containing a build and an equipment.
        return build, equipment


if __name__ == "__main__":
    snowcrows = Snowcrows()
    profession_name = "<PROFESSION_NAME>"
    build_names = snowcrows.get_build_names(profession_name)
    print(f"Available builds for {profession_name}:")
    for build_name in build_names:
        print(f"- {build_name}")
