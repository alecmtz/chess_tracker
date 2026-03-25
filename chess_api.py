import requests


class ChessAPI:

    def __init__(self):
        self.base_url = "https://ratings-api.uschess.org/api/v1/members/"

    def get_tournament_data(self, player_id):
        """" Returns json with tournament data """
        url = f"{self.base_url}{player_id}/sections?Offset=0&Size=50"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


