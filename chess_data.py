class ChessData:
    """
    Transforms raw US Chess API tournament data for a single player into
    a structured format ready for upload to Google Sheets.

    Handles merging of event info and rating records, filtering to relevant
    fields, and ordering values into upload-ready rows.
    """

    TOURNAMENT_KEYS_OF_INTEREST = {"studentId", "endDate", "stateCode", "name", "sectionName",
                                   "ratingSource", "preRating", "postRating"}
    TOURNAMENT_ORDERED_KEYS = ["studentId", "endDate", "stateCode", "name", "sectionName",
                               "ratingSource", "preRating", "postRating"]

    def __init__(self, chess_data: list, player_id: int):
        """
        Args:
            chess_data: List of raw tournament dicts returned from the US Chess API.
            player_id: The US Chess member ID for this player.
        """
        self.player_id = player_id
        self.data = chess_data  # Pass all tournaments as a list of dictionaries
        self.tournament_data = self._format_tournament_data(self.data, self.player_id)

    def get_tournament_data(self) -> list:
        """Returns the formatted list of tournament dicts with keys of interest."""
        return self.tournament_data

    def _format_tournament_data(self, data_to_format: list, player_id: int) -> list:
        # @TODO: fix docstrings
        """
        Flattens raw API tournament data into a list of dicts containing only keys of interest.

        For each tournament, merges event info and each rating record into a single dict,
        then filters to KEYS_OF_INTEREST. Tournaments with multiple rating records
        (e.g. Regular + Quick) produce one dict per record.

        Args:
            data_to_format: Raw list of tournament dicts from the US Chess API.
            player_id: The US Chess member ID to attach to each record.

        Returns:
            A list of flat dicts, one per rating record, containing only KEYS_OF_INTEREST.
        """
        tournament_data = []

        # Get dictionaries
        for tournament in data_to_format:

            # Get event and rating information
            rating_records = tournament.get("ratingRecords")
            # Create a copy of event info and add player id and section name
            event_info = {**tournament.get("event"), "studentId": player_id,
                          "sectionName": tournament.get("sectionName")}

            # Combine the rating records and event info into a single dictionary with all the keys
            for one_record in rating_records:
                combine = {**one_record, **event_info}

                # Add it to the list only with the keys of interest
                tournament_data.append({key: value for key, value in combine.items()
                                        if key in ChessData.TOURNAMENT_KEYS_OF_INTEREST})

            # Organize data for upload
            tournament_data = self._organize_data(data=tournament_data, ordered_keys=ChessData.TOURNAMENT_ORDERED_KEYS)

        return tournament_data

    @staticmethod
    def _organize_data(ordered_keys: list, data: list) -> list:
        """
        Converts a list of dicts into ordered rows for upload.

        Each row is a flat list of values in column order with keys stripped out.

        Returns:
            A 2D list where each inner list represents one data row.
        """

        return [
            [
                dictionary.get(k) for k in ordered_keys
            ]
            for dictionary in data
        ]


