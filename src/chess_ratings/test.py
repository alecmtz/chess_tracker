# import requests
#
# url = "https://ratings-api.uschess.org/api/v1/members/31619200/sections?Offset=0&Size=10"
# r = requests.get(url, timeout=10)
# print(r.status_code)
# print(dict(r.headers))
# print("*******")
# print(r.json())

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT
print(DATA_DIR)
