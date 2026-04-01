
def format_tournament_data(data_to_format, player_id) -> list:
    tournament_data = []
    keys_of_interest = {"studentId", "endDate", "stateCode", "name", "sectionName",
                        "ratingSource", "preRating", "postRating"}

    # Get dictionaries
    for tournament in data_to_format:

        # Get data of interest
        rating_records = tournament.get("ratingRecords")
        event_info = tournament.get("event")

        # Add player id and section name information into the dictionary
        event_info["studentId"] = player_id
        event_info["sectionName"] = tournament.get("sectionName")

        # Combine the rating records and event info into a single dictionary with all the keys
        for one_record in rating_records:
            combine = {**one_record, **event_info}

            # Add it to the list only with the keys of interest
            tournament_data.append({key: value for key, value in combine.items() if key in keys_of_interest})

    return tournament_data


class ChessData:

    def __init__(self, chess_data, player_id):
        self.player_id = player_id
        # self.player_id = 123456
        self.data = chess_data  # Pass all tournaments as a list
        # self.data = [{'id': '01KMDV79DBSYVYFQPV18QJ5ZBP', 'sectionNumber': 1, 'sectionName': 'Gold', 'startDate': '2026-03-21', 'endDate': '2026-03-21', 'format': 'Swiss', 'ratingSystem': 'D', 'ratingRecords': [{'eventId': '01KMDV79DBTCZFH4VSA4QJJCXQ', 'sectionNumber': 1, 'preRating': 2070, 'preRatingDecimal': 2069.64, 'postRating': 2076, 'postRatingDecimal': 2076.23, 'ratingSource': 'R'}, {'eventId': '01KMDV79DBTCZFH4VSA4QJJCXQ', 'sectionNumber': 1, 'preRating': 1865, 'preRatingDecimal': 1864.92, 'postRating': 1882, 'postRatingDecimal': 1881.86, 'ratingSource': 'Q'}], 'event': {'id': '202603210453', 'name': 'Evanston 3x3 3/21/2026', 'startDate': '2026-03-21', 'endDate': '2026-03-21', 'stateCode': 'IL'}}, {'id': '01KKQH9YN2JTQT9E67DX8NGFCQ', 'sectionNumber': 1, 'sectionName': 'Open', 'startDate': '2026-03-14', 'endDate': '2026-03-14', 'format': 'Swiss', 'ratingSystem': 'D', 'ratingRecords': [{'eventId': '01KKQH9YMWPSY2A6Z4SXQB4FCX', 'sectionNumber': 1, 'preRating': 2085, 'preRatingDecimal': 2084.89, 'postRating': 2070, 'postRatingDecimal': 2069.64, 'ratingSource': 'R'}, {'eventId': '01KKQH9YMWPSY2A6Z4SXQB4FCX', 'sectionNumber': 1, 'preRating': 1875, 'preRatingDecimal': 1874.64, 'postRating': 1865, 'postRatingDecimal': 1864.92, 'ratingSource': 'Q'}], 'event': {'id': '202603140963', 'name': 'March $1,000 Open 2026', 'startDate': '2026-03-14', 'endDate': '2026-03-14', 'stateCode': 'WI'}}]

        self.tournament_data = format_tournament_data(self.data, self.player_id)
        self.data_to_upload = self.organize_data()

    def get_tournament_data(self):
        return self.tournament_data

    def get_data_to_upload(self):
        return self.data_to_upload

    def organize_data(self) -> list:
        t_data = self.get_tournament_data()
        final_list = []

        for t in t_data:
            prepare_data = [
                t.get("studentId"),
                t.get("endDate"),
                t.get("stateCode"),
                t.get("name"),
                t.get("sectionName"),
                t.get("ratingSource"),
                t.get("preRating"),
                t.get("postRating"),
            ]
            final_list.append(prepare_data)

        return final_list


# chess = ChessData()
# d = chess.get_data_to_upload()
# print(d)


