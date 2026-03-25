from chess_api import ChessAPI
from google_sheets import GoogleSheets
from chess_data import ChessData

# Initialize google sheets
gs = GoogleSheets()
student_id = gs.get_student_ids()[0]  # Get single student for testing

# Call us chess org
api = ChessAPI()
tournament_data = api.get_tournament_data(player_id=student_id)

chess_data = ChessData(chess_data=tournament_data, days=1, player_id=student_id)
data_to_upload = chess_data.get_data_to_upload()
gs.update_tournament_sheet(data_to_upload=data_to_upload)

