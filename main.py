import time
from datetime import datetime, timedelta
from chess_api import ChessAPI
from google_sheets import GoogleSheets
from chess_data import ChessData


def main():
    # Initialize google sheets and chess org
    gs = GoogleSheets()
    api = ChessAPI()

    # Initialize arrays
    player_tournament_data = []
    transform_data = []

    # STEP 1: Extract data
    # Get student ids from Google sheets
    student_ids = gs.get_student_ids()[:3]  # Get 2 students for testing
    print(f"Student ids: {student_ids}")

    # Get one week worth of tournament data
    one_week_ago = str(datetime.today().date() - timedelta(weeks=1))

    # Go over each student
    for player_id in student_ids:
        # Call the api
        tournament_data = api.get_tournament_data(player_id=player_id)
        # time.sleep(1)

        # Check that data is not empty
        if tournament_data is not None:
            # Get tournament data
            t_data = tournament_data.get("items")  # This is a list with dictionaries

            # Only get last week
            last_weekend_tournaments = [
                tournament
                for tournament in t_data
                if tournament.get("endDate") >= one_week_ago
            ]

            # Add tournament data with the student's id
            player_tournament_data.append((last_weekend_tournaments, player_id))

    # Step 2: Transform data
    # This returns 3 nested arrays
    for player_data in player_tournament_data:  # Get values from the list to pass to ChessData
        transform_data.append(ChessData(chess_data=player_data[0], player_id=player_data[1]).get_data_to_upload())

    # Convert to 2D array for Google sheets
    flat_data = [
        item for sublist in transform_data for item in sublist
    ]

    # Step 3: Load data
    # Upload to google sheets
    gs.update_tournament_sheet(data_to_upload=flat_data)


if __name__ == "__main__":
    main()
