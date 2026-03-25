import gspread
import pandas as pd


SPREADSHEET_ID = "1PuM3GgFI9z6B0_WU3itMjzDcihk5C1KaT1i0CXIXI7E"


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
        self.student_sheet = self.gc.open_by_key(SPREADSHEET_ID).worksheet("Student Information")
        self.tournament_sheet = self.gc.open_by_key(SPREADSHEET_ID).worksheet("Tournaments")
        self.student_ids = self.get_student_ids()

    def update_tournament_sheet(self, data_to_upload):
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
        self.tournament_sheet.append_rows(final_list)

    def get_student_spreadsheet(self):
        """"Returns spreadsheet as a dataframe"""
        df = convert_to_df(self.student_sheet)
        return df

    def get_student_ids(self) -> list:
        """"Returns student's ids"""
        df = self.get_student_spreadsheet()
        return df.get("student_id").to_list()


