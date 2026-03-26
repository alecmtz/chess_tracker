import gspread
import datetime as dt
import pandas as pd


SPREADSHEET_ID = "1PuM3GgFI9z6B0_WU3itMjzDcihk5C1KaT1i0CXIXI7E"
NUM_COLUMNS = 8
COLUMN_TITLES = ["Student Id", "Tournament End Date", "Tournament State", "Event", "Section", "Rating System",
                 "Pre-Rating", "Post-Rating"]


def convert_to_df(datasheet):
    # Convert into a dataframe
    df = pd.DataFrame(data=datasheet.get_all_records())

    # Clean columns
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace("-", "_")
    df.columns = df.columns.str.lower()
    return df


class GoogleSheets:

    def __init__(self):
        # Get access to google account
        self.gc = gspread.service_account(filename="service_account.json")

        # Get the sheets
        self.spreadsheet = self.gc.open_by_key(SPREADSHEET_ID)
        self.student_sheet = self.spreadsheet.worksheet("Student Information")
        self.student_ids = self.get_student_ids()

        # Get today's date
        self.today = dt.date.today()

    def update_tournament_sheet(self, data_to_upload):
        """" Creates new sheet with new tournament data """
        final_list = []
        for dictionary in data_to_upload:
            new_list = [
                dictionary["student_id"],
                dictionary["endDate"],
                dictionary["stateCode"],
                dictionary["name"],
                dictionary["sectionName"],
                dictionary["ratingSource"],
                dictionary["preRating"],
                dictionary["postRating"],
            ]
            final_list.append(new_list)
        tournament_sheet = self.create_new_tournament_sheet(rows_of_data=final_list)
        tournament_sheet.append_rows(final_list)
        print("Data was uploaded successfully")

    def create_new_tournament_sheet(self, rows_of_data):
        """" Creates a new tournament sheet with today's date and returns it """
        len_data = len(rows_of_data) + 10  # Added 10 for extra buffering
        print(f"Len of rows: {len_data}")
        tournament_sheet = self.spreadsheet.add_worksheet(title=f"{self.today}", rows=len_data, cols=NUM_COLUMNS)
        tournament_sheet.append_row(COLUMN_TITLES)
        print(f"New sheet has been created with today's date: {self.today}")
        return tournament_sheet

    def get_student_spreadsheet(self):
        """"Returns spreadsheet as a dataframe"""
        df = convert_to_df(self.student_sheet)
        return df

    def get_student_ids(self) -> list:
        """"Returns student's ids"""
        df = self.get_student_spreadsheet()
        return df.get("student_id").to_list()


