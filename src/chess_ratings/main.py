import json
import time
import csv
import transform
import pandas as pd

from datetime import datetime, timedelta
from collections import Counter

from chess_api import ChessAPI
from google_sheets import GoogleSheets
from raw_storage import RawStorage


MAX_CONSECUTIVE_RATE_LIMITS = 5
AGES = ["7andUnder", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]  # "Under21", "50Plus", "65Plus"]

# Initialize google sheets, chess org and data store
google_sheets = GoogleSheets()
chess_api = ChessAPI()


def get_student_ids(gs: GoogleSheets) -> list:
    return gs.get_students().get("student_id").to_list()


def get_updated_ids(ids: list, raw_data: RawStorage):
    # Load data
    data = raw_data.load()

    # Cache local var
    student_ids = ids
    if data:
        print(f"Resuming: {len(data)} players already saved today {datetime.today().date()}")
        for existing_id in data:
            student_ids.remove(existing_id)

    return student_ids


def call_us_chess_data(raw_data: RawStorage, data_request: str, student_ids: list):  # (data_request: str | None, ids: list | None):
    count = 0
    unknown_ids = []

    len_student_ids = len(student_ids)

    if data_request == "tournament":

        for player_id in student_ids:
            # Call the API
            api_response = chess_api.get_tournament_data(player_id=player_id)

            # If we get data back save on disk immediately
            if api_response is not None:
                raw_data.save(player_id=player_id, data=api_response)
                count += 1
                print(f"COMPLETED: {count}/{len_student_ids}")
            else:
                unknown_ids.append(player_id)
                print(f"NOT COMPLETED: {len(unknown_ids)}")
    elif data_request == "100":
        for age in AGES[:1]:
            # Call the API
            api_response = chess_api.get_top_players(age=age)

            print(api_response)
            print("\n" * 20)

            if api_response is not None:
                raw_data.save(data=api_response)


def main():
    print("\n****************** WELCOME TO THE LIFE OF AUTOMATION ******************\n")

    done = False
    while not done:
        user_answer = input("Type 'tournament' or '100' (top-100) or 'exit': ").lower()

        if user_answer == 'exit':
            done = True
        elif user_answer == 'tournament' or '100':
            # Initialize storage
            raw_data = RawStorage(section=user_answer)

            # Start time
            start = time.time()

            # ---------------- STEP 1: Extract Data ----------------
            # Fetch student IDS
            student_ids = get_student_ids(gs=google_sheets)

            # Check if there's existing data before calling API
            updated_ids = get_updated_ids(ids=student_ids, raw_data=raw_data)
            if updated_ids:
                call_us_chess_data(data_request=user_answer, student_ids=updated_ids, raw_data=raw_data)

            call_us_chess_data(data_request=user_answer, student_ids=student_ids, raw_data=raw_data)

            # ---------------- STEP 2: Load / Transform Data ----------------
            # Load data
            # saved_data = get_load_data()

            # # Transform raw data into a dataframe
            # df = transform.to_dataframe(saved_data=saved_data, section=user_answer)
            #
            # # Get last week tournament data
            # df = transform.filter_recent(df=df, days=8)
            # print(df)
            #
            # # ---------------- Step 3: Load data ----------------
            # # Upload to google sheets
            # google_sheets.load_tournament_data(df=df)
            #
            # # ---------------- Stop Timer ----------------
            # elapsed = time.time() - start
            # minutes = int(elapsed // 60)
            # seconds = int(elapsed % 60)
            # print(f"Total runtime: {minutes}m {seconds}s")

        else:
            print("Whooops.. try again. Please type 'tournament' or '100'")


if __name__ == "__main__":
    main()
