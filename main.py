import time
import csv
from datetime import datetime, timedelta
from chess_api import ChessAPI
from google_sheets import GoogleSheets
from chess_data import ChessData


def flat_data(data: list):
    # Convert to 2D array for Google sheets
    return [
        item for sublist in data for item in sublist
    ]


def get_top_players(gs, api):
    final_list_top_players = []
    ages = ["7andUnder", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]  # "Under21", "50Plus", "65Plus"]
    completed = 0
    not_completed = 0

    # Get students ids from Google Sheets
    student_ids = gs.get_student_ids()

    for age in ages:
        # Get the 100 players list
        api_response = api.get_top_players(age=age)

        if api_response is not None:
            top_players_data = api_response.get("topPlayers")

            # Space out requests
            time.sleep(0.2)

            chess_data = ChessData(top_players_data=(top_players_data, age), player_id=student_ids)
            final_list_top_players.append(chess_data.get_top_players())

            completed += 1
            print(f"REGULAR {age} COMPLETED. {completed}/{len(ages)}")
        else:
            not_completed += 1
            print(f"REGULAR {age} NOT COMPLETED. {not_completed}/{not_completed}")


    print(final_list_top_players)

    # Convert to 2D array for Google sheets
    final_list_top_players = flat_data(final_list_top_players)

    print(final_list_top_players)


    gs.update_top_player_sheet(data_to_upload=final_list_top_players)


def get_tournament_data(gs, api):
    # Start timer
    start = time.time()

    # Initialize arrays
    player_tournament_data = []
    transform_data = []

    # Initialize count
    count = 0
    unknown_ids = []

    # STEP 1: Extract data
    # Get student ids from Google sheets
    student_ids = gs.get_student_ids()
    len_student_ids = len(student_ids)
    print(f"Number of player id's from google sheet: {len_student_ids}")

    # Get one week worth of tournament data
    one_week_ago = str(datetime.today().date() - timedelta(weeks=1))

    # Go over each student
    for player_id in student_ids:
        # Call the api
        api_response = api.get_tournament_data(player_id=player_id)

        # Space out requests
        time.sleep(0.2)

        # Check that data is not empty
        if api_response is not None:
            # Get tournament data
            tournament_data = api_response.get("items")  # This is a list with dictionaries

            # Only get last week, empty [] gets added when the condition is not met
            last_weekend_tournaments = [
                tournament
                for tournament in tournament_data
                if tournament.get("endDate") >= one_week_ago
            ]

            # Add tournament data with the student's id and filter out empty [] to avoid a None crash in chess_data
            if last_weekend_tournaments:
                player_tournament_data.append((last_weekend_tournaments, player_id))

            count += 1
            print(f"COMPLETED: {count}/{len_student_ids}")
        else:
            unknown_ids.append(player_id)
            print(f"NOT COMPLETED: {len(unknown_ids)}")

    # Step 2: Transform data
    # This returns 3 nested arrays
    for player_data in player_tournament_data:  # Get values from the list to pass to ChessData
        transform_data.append(ChessData(tournament_data=player_data[0],
                                        player_id=player_data[1]).get_tournament_data())

    # Convert to 2D array for Google sheets
    final_tournament_list = flat_data(transform_data)

    # Step 3: Load data
    # Upload to google sheets
    gs.update_tournament_sheet(data_to_upload=final_tournament_list)

    print("****************** END OF THE PROGRAM ******************\n")
    print("                   (Now a sassy dance)                   \n")

    today = datetime.today().date()
    if unknown_ids:
        print("**************** REPORT FOR MISSING IDS ****************\n")
        print(f"Missing data for {len(unknown_ids)} IDs:")

        with open(f"missing_ids_{today}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["player_id"])
            for player_id in unknown_ids:
                print(f"Missing: {player_id}")
                writer.writerow([player_id])
        print(f"Missing IDs exported to missing_ids_{today}.csv")

    elapsed = time.time() - start
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    print(f"Total runtime: {minutes}m {seconds}s")


def main():
    print("\n****************** WELCOME TO THE LIFE OF AUTOMATION ******************\n")

    # Initialize google sheets and chess org
    google_sheets = GoogleSheets()
    chess_pi = ChessAPI()

    done = False
    while not done:
        user_answer = input("Type 'tournament' or '100' (top-100) or 'exit': ").lower()

        if user_answer == 'tournament':
            get_tournament_data(gs=google_sheets, api=chess_pi)
            done = True
        elif user_answer == '100':
            get_top_players(gs=google_sheets, api=chess_pi)
            done = True
        elif user_answer == 'exit':
            done = True
        else:
            print("Whooops.. try again. Please type 'tournament' or '100'")


if __name__ == "__main__":
    main()
