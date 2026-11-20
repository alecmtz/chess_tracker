from unittest.mock import patch
import requests
from src.chess_ratings.chess_api import ChessAPI


def fake_429(retry_after=None):
    resp = requests.Response()
    resp.status_code = 429
    if retry_after:
        resp.headers["Retry-After"] = retry_after
    return resp


for header in ("7", None):
    api = ChessAPI()
    with patch("chess_api.requests.get", return_value=fake_429(header)), \
         patch("chess_api.time.sleep") as fake_sleep:
        result = api.get_tournament_data(12345)

    print(f"Retry-After={header}")
    print("  result:", result)
    print("  failed:", api.failed)
    print("  sleeps:", [c.args[0] for c in fake_sleep.call_args_list])