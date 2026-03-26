

def format_rating_records_data(data_to_format) -> list:
    """" Returns a list of dictionaries with the tournaments information """
    get_rating_records = data_to_format.get("ratingRecords")
    keys_of_interest = {"preRating", "postRating", "ratingSource"}
    new_list = [
        {key: value for key, value in dictionary.items() if key in keys_of_interest}
        for dictionary in get_rating_records
    ]
    return new_list


def format_event_data(data_to_format) -> dict:
    """ Returns new dictionary with the event information """
    get_event = data_to_format.get("event")
    keys_of_interest = {"name", "endDate", "stateCode"}
    new_dict = {key: value for key, value in get_event.items() if key in keys_of_interest}
    new_dict["sectionName"] = data_to_format.get("sectionName")
    return new_dict


class ChessData:

    def __init__(self, chess_data, player_id):
        self.player_id = player_id
        self.data = chess_data.get("items")[0]  # Get the last tournament played
        self.rating_records = format_rating_records_data(self.data)
        self.event_records = format_event_data(self.data)
        self.data_to_upload = self.organize_data()

    def get_rating_records(self):
        return self.rating_records

    def get_event_info(self):
        return self.event_records

    def get_data_to_upload(self):
        return self.data_to_upload

    def organize_data(self) -> list:
        ratings = self.get_rating_records()
        event = self.get_event_info()

        # Add player id on the dictionary event
        event["student_id"] = self.player_id

        # Get the structure flat
        flat_the_data = [
            {**dic, **event}
            for dic in ratings
            ]

        # Only grab keys of interest
        data = []
        for dictionary in flat_the_data:
            build_list = [
                dictionary["student_id"],
                dictionary["endDate"],
                dictionary["stateCode"],
                dictionary["name"],
                dictionary["sectionName"],
                dictionary["ratingSource"],
                dictionary["preRating"],
                dictionary["postRating"],
            ]
            data.append(build_list)
        return data



