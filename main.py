import time
from datetime import datetime, timedelta
from chess_api import ChessAPI
from google_sheets import GoogleSheets
from chess_data import ChessData

# Initialize google sheets
gs = GoogleSheets()
student_ids = gs.get_student_ids()  # Get 2 students for testing
print(f"Student ids: {student_ids}")

# Initialize chess org api
api = ChessAPI()

# Extract data from US Chess
one_week_ago = datetime.today() - timedelta(weeks=1)
all_raw_data = []
for chess_id in student_ids:
    # Call the api to get the data
    tournament_data = api.get_tournament_data(player_id=chess_id)
    print(f"Data extracted for: {chess_id}")
    # time.sleep(1)

    # Get tournament date
    tournament_date = datetime.strptime(tournament_data.get("items")[0].get("endDate"), "%Y-%m-%d")

    # Compare date with a week ago
    if tournament_date >= one_week_ago:
        all_raw_data.append((chess_id, tournament_data))

print(f"raw data: {all_raw_data}")
# Transform data - this returns 3 nested arrays
all_formatted = [
    ChessData(chess_data=data, player_id=chess_id).get_data_to_upload()
    for chess_id, data in all_raw_data # I need to extract this values from the list to pass the to ChessData
    ]

print(f"all formated: {all_formatted}")

# Simplify structure as 2 nested arrays for google upload to work
flat = [item for sublist in all_formatted for item in sublist]
print(flat)
gs.update_tournament_sheet(data_to_upload=flat)

