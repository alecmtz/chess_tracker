import time
import requests
from requests import RequestException


class ChessAPI:
    """
    Client for the US Chess ratings API.

    Fetches tournament section data for individual players with built-in
    retry logic for rate limit responses.
    """
    BASE_URL = "https://ratings-api.uschess.org/api/v1/members/"
    DEFAULT_SIZE = 10
    TIMEOUT = 10
    SLEEP = 5

    def __init__(self):
        """ Initializes the client with the US Chess ratings API base URL """
        self.base_url = ChessAPI.BASE_URL

    def get_tournament_data(self, player_id: int, retries: int = 3) -> dict | None:
        """
        Fetches tournament section data for a given player from the US Chess ratings API.

        Retries up to `retries` times if the API returns a 429 rate limit response,
        waiting 5 seconds between attempts.

        Args:
            player_id: The US Chess member ID to fetch tournament data for.
            retries: Maximum number of retry attempts on a 429 response. Defaults to 3.

        Returns:
            A dict containing the API response with a list of tournament sections,
            or None if the request fails, the player has no data, or retries are exhausted.
        """

        url = f"{self.base_url}{player_id}/sections?Offset=0&Size={ChessAPI.DEFAULT_SIZE}"
        try:
            response = requests.get(url, timeout=ChessAPI.TIMEOUT)  # raises timeout after 10 seconds
            response.raise_for_status()
        except RequestException as error:
            if error.response is not None and error.response.status_code == 429:  # hitting rate limit
                time.sleep(ChessAPI.SLEEP)
                retries -= 1
                if retries == 0:
                    print(f"Max number of retries reached for player {player_id}")
                    return None
                return self.get_tournament_data(player_id, retries)  # retry
            print(f"Request failed for player {player_id}: {error}")
            return None
        else:
            res = response.json()
            if self._is_empty(data=res):
                print(f"No information found for member: {player_id}. Skipping ...")
                return None
            return res

    @staticmethod
    def _is_empty(data: dict) -> bool:
        """
        Checks whether the API response contains no tournament data.

        Args:
            data: The parsed JSON response from the API.

        Returns:
            True if the items list is missing or empty, False otherwise.
        """
        return len(data.get("items", [])) == 0

