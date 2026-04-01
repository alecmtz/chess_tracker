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
one_week_ago = str(datetime.today().date() - timedelta(weeks=1))
print(f"2 week ago: {one_week_ago}")
last_weekend_tournaments = []
player_tournament_data = []
keys_of_interest = {"endDate", "stateCode", "name", "ratingSource", "preRating", "postRating", "studentId"}

for chess_id in student_ids:
    # Call the api to get the data
    tournament_data = api.get_tournament_data(player_id=chess_id)
    # time.sleep(1)

    # Get tournament data
    t_data = tournament_data.get("items")  # This is a list with dictionaries
    # print(f"t_data: {t_data}")

    last_weekend_tournaments = [
        {key: value for key, value in tournament.items()}
        for tournament in t_data
        if tournament.get("endDate") >= one_week_ago
    ]
    # print(f"last weekend tournament data: {last_weekend_tournaments}")
    player_tournament_data.append((last_weekend_tournaments, chess_id))  # FIX - appends empty [], 123456
    # print(f"player tournament: {player_tournament_data}")


# Transform data - this returns 3 nested arrays
transform_data = []
for data in player_tournament_data:  # I need to extract this values from the list to pass to ChessData
    print(f"data in transform phase: {data}")
    transform_data.append(ChessData(chess_data=data[0], player_id=data[1]).get_data_to_upload())

flat_data = [
    item for sublist in transform_data for item in sublist
]

print(flat_data)


# upload to work
gs.update_tournament_sheet(data_to_upload=flat_data)

