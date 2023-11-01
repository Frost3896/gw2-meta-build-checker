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
        """Request website content and parse it into a BeautifulSoup object."""
        website = requests.get(url, headers=self._HEADERS)
        return BeautifulSoup(website.content, "html.parser")

    def _parse_build(self) -> Build:
        # To be done
        return build

    def _parse_equipment(self) -> Equipment:
        # To be done
        return equipment

    @functools.lru_cache(maxsize=None)
    def get_build_names(self, profession_name: str) -> list[str]:
        """Get a list of build names for the specified profession name."""
        # Convert profession name to lowercase.
        profession_name = profession_name.lower()
        # Retrieve build names from both featured and beginner categories.
        build_names = []
        for category in ["featured", "beginner"]:
            # Assemble URL and request html content.
            url = (
                f"{self._BASE_URL}"
                f"{profession_name}?category={category}"
            )
            html_content = self._get_html_content(url)
            # Extract text from <h2> elements, excluding "Related guides".
            h2_elements = [
                element.text
                for element in html_content.find_all("h2")
                if "Related guides" not in element.text
            ]
            # Remove trailing whitespace in text from <h2> elements.
            for i in range(len(h2_elements)):
                h2_elements[i] = h2_elements[i].rstrip()
            # Append text from <h2> elements to build names.
            build_names.extend(h2_elements)
        return build_names

    @functools.lru_cache(maxsize=None)
    def get_build(self, profession_name: str, build_name: str) -> Build:
        """Get detailed build information for a specific build name."""
        # Convert profession name to lowercase.
        profession_name = profession_name.lower()
        # Convert build name to lowercase and replace space with hyphen.
        build_name = build_name.lower().replace(" ", "-")
        # Extract specialization name from build name.
        specialization_name = build_name.rsplit("-", 1)[-1]
        # Assemble URL and request html content.
        url = (
            f"{self._BASE_URL}"
            f"{profession_name}/{specialization_name}/{build_name}"
        )
        html_content = self._get_html_content(url)
        return None


if __name__ == "__main__":
    snowcrows = Snowcrows()
    profession_name = "<PROFESSION_NAME>"
    build_names = snowcrows.get_build_names(profession_name)
    print(f"Available builds for {profession_name}:")
    for build_name in build_names:
        print(f"- {build_name}")
