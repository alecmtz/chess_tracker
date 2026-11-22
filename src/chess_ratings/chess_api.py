import time
import requests
from requests import RequestException


class ChessAPI:
    """
    Client for the US Chess ratings API.

    Fetches tournament section data for individual players with built-in
    retry logic for rate limit responses.
    """
    BASE_ENDPOINT = "https://ratings-api.uschess.org/api/v1/"
    MEMBERS_ENDPOINT = "members/"
    TOP_PLAYERS_ENDPOINT = "top-players/Regular"
    DEFAULT_SIZE = 10
    TIMEOUT = 10

    MAX_ATTEMPTS = 5
    BASE_DELAY = 5  # seconds before the first retry; doubles each time
    MAX_DELAY = 120  # cap on any single wait
    REQUEST_INTERVAL = 0.5  # polite pause before every request
    RATE_LIMITED = "rate limited (retries exhausted)"

    def __init__(self):
        """ Initializes the client with the US Chess ratings API base URL """
        self.base_endpoint = ChessAPI.BASE_ENDPOINT
        self.failed = {}  # id/label -> reason, summarized once at the end of the run

    def _get(self, url: str, label) -> requests.Response | None:
        """GET with throttling and backoff on 429. Records the reason on failure."""
        for attempt in range(ChessAPI.MAX_ATTEMPTS):
            time.sleep(ChessAPI.REQUEST_INTERVAL)
            try:
                response = requests.get(url, timeout=ChessAPI.TIMEOUT)
                response.raise_for_status()
                return response
            except RequestException as error:
                status = error.response.status_code if error.response is not None else None
                if status != 429:
                    self.failed[label] = f"request error: {error}"
                    print(f"Request failed for {label}: {error}")
                    return None
                if attempt < ChessAPI.MAX_ATTEMPTS - 1:   # don't sleep after the last try
                    delay = self._backoff_delay(error.response, attempt)
                    print(f"Rate limited on {label}, waiting {delay}s "
                          f"(attempt {attempt + 1}/{ChessAPI.MAX_ATTEMPTS})")
                    time.sleep(delay)
        self.failed[label] = ChessAPI.RATE_LIMITED
        print(f"Max number of retries reached for {label}")
        return None

    @staticmethod
    def _backoff_delay(response: requests.Response, attempt: int) -> float:
        print(" ***** _backoff_delay ******")
        print(response)
        print(response.headers)
        retry_after = response.headers.get("Retry-After")
        if retry_after and retry_after.isdigit():
            return min(int(retry_after), ChessAPI.MAX_DELAY)
        return min(ChessAPI.BASE_DELAY * 2 ** attempt, ChessAPI.MAX_DELAY)

    def get_tournament_data(self, player_id: int) -> dict | None:
        url = (f"{self.base_endpoint}{ChessAPI.MEMBERS_ENDPOINT}"
               f"{player_id}/sections?Offset=0&Size={ChessAPI.DEFAULT_SIZE}")
        response = self._get(url, label=player_id)

        if response is None:
            return None

        res = response.json()
        if not res.get("items"):
            self.failed[player_id] = "no data found"
            print(f"No information found for member: {player_id}. Skipping ...")
            return None

        return res

    def get_top_players(self, age: int) -> dict | None:
        url = f"{self.base_endpoint}{ChessAPI.TOP_PLAYERS_ENDPOINT}{age}"
        response = self._get(url, label=f"top players Regular {age}")

        if response is None:
            return None

        res = response.json()
        if not res.get("topPlayers"):
            self.failed[f"top players Regular {age}"] = "no data found"
            print(f"No information found for top-100 Regular {age}. Skipping ...")
            return None
        return res

