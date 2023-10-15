import requests
import functools


class API:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._clear_cache()

    def _clear_cache(self):
        # Clear the cache for methods that need to be invalidated
        self.get_account_name.cache_clear()
        self.get_character_names.cache_clear()
        self.get_profession_name.cache_clear()

    def set_api_key(self, api_key: str):
        if self.api_key != api_key:
            self.api_key = api_key
            self._clear_cache()

    def get_endpoint_v2(self, endpoint: str):
        url = f"https://api.guildwars2.com/v2/{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        return requests.get(url, headers=headers).json()

    def check_key(self) -> bool:
        # check if api key is valid
        tokeninfo = self.get_endpoint_v2("tokeninfo")
        if tokeninfo == "Invalid access token":
            return False
        # check if correct permissions are set
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
        account_name = self.get_endpoint_v2("account")
        return account_name["name"]

    @functools.lru_cache(maxsize=None)
    def get_character_names(self) -> list[str]:
        character_names = self.get_endpoint_v2("characters")
        return character_names

    @functools.lru_cache(maxsize=None)
    def get_profession_name(self, character: str) -> str:
        profession_name = self.get_endpoint_v2(
            f"characters/{character}/core"
        )
        return profession_name["profession"]

    @functools.lru_cache(maxsize=None)
    def get_specialization_name(self, specialization_id: int) -> str:
        specialization_name = self.get_endpoint_v2(
            f"specializations/{specialization_id}"
        )
        return specialization_name["name"]

    @functools.lru_cache(maxsize=None)
    def get_skill_name(self, skill_id: int) -> str:
        skill_name = self.get_endpoint_v2(f"skills/{skill_id}")
        return skill_name["name"]

    @functools.lru_cache(maxsize=None)
    def get_trait_name(self, trait_id: int) -> str:
        trait_name = self.get_endpoint_v2(f"traits/{trait_id}")
        return trait_name["name"]

    def get_build_templates(self, character: str):
        build_templates = self.get_endpoint_v2(
            f"characters/{character}/buildtabs?tabs=all"
        )
        return build_templates

    def get_equipment_templates(self, character: str):
        equipment_templates = self.get_endpoint_v2(
            f"characters/{character}/equipmenttabs?tabs=all"
        )
        return equipment_templates


if __name__ == "__main__":
    api = API("API-KEY")
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
