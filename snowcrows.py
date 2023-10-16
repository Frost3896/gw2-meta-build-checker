import requests
import functools
from bs4 import BeautifulSoup


class Snowcrows:
    def __init__(self) -> None:
        self.base_url = "https://snowcrows.com/builds"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) "
                "Gecko/20100101 Firefox/118.0"
            )
        }
        self._clear_cache()

    def _clear_cache(self) -> None:
        # Clear the cache for methods that need to be invalidated
        self.get_build_names.cache_clear()
        self.get_build.cache_clear()

    def _get_html_content(self, url: str) -> BeautifulSoup:
        # Request website and parse content
        website = requests.get(url, headers=self.headers)
        return BeautifulSoup(website.content, "html.parser")

    def _parse_build(self) -> None:
        # To be done
        pass

    @functools.lru_cache(maxsize=None)
    def get_build_names(self, profession_name: str) -> list[str]:
        build_names = []
        for category in ["recommended", "effective"]:
            # Prepare request for the category
            url = (
                f"{self.base_url}"
                f"?profession={profession_name}&category={category}"
            )
            # Get html content for the url
            html_content = self._get_html_content(url)
            # Find all <h2> elements that do not contain "Related guides"
            h2_elements = [
                element.text
                for element in html_content.find_all("h2")
                if "Related guides" not in element.text
            ]
            # Append text from <h2> elements to the build_names list
            build_names.extend(h2_elements)
        return build_names

    @functools.lru_cache(maxsize=None)
    def get_build(self, profession_name: str, build_name: str):
        build_name = build_name.lower().replace(" ", "-")
        # Prepare request
        url = (
            f"{self.base_url}"
            f"/{profession_name}/{build_name}"
        )
        # Get html content for the url
        html_content = self._get_html_content(url)
        # To be continued...


if __name__ == "__main__":
    snowcrows = Snowcrows()
    profession_name = "Thief"
    build_names = snowcrows.get_build_names(profession_name)
    print(f"Available builds for {profession_name}:")
    for name in build_names:
        print(name)
