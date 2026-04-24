import gspread
import datetime as dt
import pandas as pd
from gspread.exceptions import WorksheetNotFound


class GoogleSheets:
    """
    Handles all interactions with the chess tracker Google Spreadsheet.

    Manages reading student data from the Student Information sheet
    and writing tournament results to dated worksheet tabs.
    """

    SPREADSHEET_ID = "1PuM3GgFI9z6B0_WU3itMjzDcihk5C1KaT1i0CXIXI7E"
    SERVICE_ACCOUNT = "service_account_susan.json"
    STUDENT_WORKSHEET = "Student Information"
    NUM_COLUMNS = 8
    COLUMN_TITLES = ["Student Id", "Tournament End Date", "Tournament State", "Event", "Section", "Rating System",
                     "Pre-Rating", "Post-Rating"]

    def __init__(self):
        """
        Authenticates with Google Sheets via a service account and loads
        the main spreadsheet and student worksheet.
        """
        # Get access to google account
        self.gc = gspread.service_account(filename=GoogleSheets.SERVICE_ACCOUNT)

        # Get the sheets
        self.spreadsheet = self.gc.open_by_key(GoogleSheets.SPREADSHEET_ID)  # Fetch the main spreadsheet
        self.student_sheet = self.spreadsheet.worksheet(GoogleSheets.STUDENT_WORKSHEET)  # Fetch the student worksheet

        # Get today's date
        self.today = dt.date.today()

    def update_tournament_sheet(self, data_to_upload: list) -> None:
        """
        Creates a new dated worksheet and uploads tournament rows to it.

        Args:
            data_to_upload: 2D list of tournament rows to append where each
                            inner list corresponds to COLUMN_TITLES order.
        """
        tournament_sheet = self.create_new_tournament_sheet(rows_of_data=data_to_upload)
        tournament_sheet.append_rows(data_to_upload)
        print("Data was uploaded successfully")

    def create_new_tournament_sheet(self, rows_of_data: list) -> gspread.Worksheet:
        """
        Creates a new worksheet titled with today's date and adds column headers.

        If a sheet for today already exists, creates a duplicate titled
        '{date} (1)' and warns the user.

        Args:
            rows_of_data: List of rows used to calculate the required sheet size.

        Returns:
            The newly created gspread Worksheet object.
        """
        len_data = len(rows_of_data) + 10  # Added 10 for extra buffering

        try:
            # Check if worksheet already exists
            self.spreadsheet.worksheet(f"{self.today}")
        except WorksheetNotFound:
            # Create a new worksheet with today's date
            tournament_sheet = self.spreadsheet.add_worksheet(title=f"{self.today}", rows=len_data,
                                                              cols=GoogleSheets.NUM_COLUMNS)
            print(f"New sheet has been created with today's date: {self.today}")
        else:
            # Create duplicate with today's date
            print(f"Warning: A sheet for {self.today} already exists. Creating duplicate '{self.today} (1)'. If you"
                  f" run it again I will crash :)")
            tournament_sheet = self.spreadsheet.add_worksheet(title=f"{self.today} (1)", rows=len_data,
                                                              cols=GoogleSheets.NUM_COLUMNS)
        tournament_sheet.append_row(GoogleSheets.COLUMN_TITLES)

        return tournament_sheet

    def get_student_spreadsheet(self) -> pd.DataFrame:
        """ Returns the Student Information worksheet as a cleaned pandas DataFrame """
        return self._convert_to_df(self.student_sheet)

    def get_student_ids(self) -> list:
        """ Returns a list of all student US Chess IDs from the Student Information sheet """
        df = self.get_student_spreadsheet()
        return df.get("student_id").to_list()

    @staticmethod
    def _convert_to_df(datasheet) -> pd.DataFrame:
        """
        Converts a gspread worksheet into a pandas DataFrame with cleaned column names.

        Column names are lowercased and spaces/hyphens replaced with underscores.

        Args:
            datasheet: A gspread Worksheet object to convert.

        Returns:
            A pandas DataFrame with normalized column names.
        """
        # Convert into a dataframe
        df = pd.DataFrame(data=datasheet.get_all_records())

        # Clean columns
        df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")
        return df

