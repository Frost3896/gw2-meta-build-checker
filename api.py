import requests


class API:
    def __init__(self, api_key: str):
        self.api_key = api_key

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
