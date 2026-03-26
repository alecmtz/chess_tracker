import time
import requests
from requests import RequestException


SIZE = 10


def is_empty(data):
    return len(data.get("items", [])) == 0


class ChessAPI:

    def __init__(self):
        self.base_url = "https://ratings-api.uschess.org/api/v1/members/"

    def get_tournament_data(self, player_id):
        """" Returns json with tournament data if empty it returns None """
        url = f"{self.base_url}{player_id}/sections?Offset=0&Size={SIZE}"
        try:
            response = requests.get(url, timeout=10)  # raises timeout after 10 seconds
            response.raise_for_status()
        except RequestException as error:
            if error.response.status_code == 429:  # hitting rate limit
                time.sleep(5)
            print(f"Request failed for player {player_id}: {error}")
            return None
        else:
            res = response.json()
            if is_empty(data=res):
                print(f"No information found for member: {player_id}. Skipping ...")
                return None
            return res

