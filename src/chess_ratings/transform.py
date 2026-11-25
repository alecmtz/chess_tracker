import pandas as pd
from datetime import date, timedelta

COLUMNS = {
    "event.endDate": "Tournament End Date",
    "event.stateCode": "Tournament State",
    "event.name": "Event",
    "sectionName": "Section",
    "ratingSource": "Rating System",
    "preRating": "Pre-Rating",
    "postRating": "Post-Rating",
}


def to_dataframe(saved_data: dict, section: str) -> pd.DataFrame:
    if section == "tournament":
        return tournament_dataframe(saved_data=saved_data)


# Private method
def tournament_dataframe(saved_data: dict) -> pd.DataFrame:
    # Create list to collect data in a cheap python container (dict), build the df once at the end
    sections = []
    for player_id, data in saved_data.items():
        if data is not None:
            for s in data["items"]:
                # Check rating records is not empty
                s.get("ratingRecords")
                # Add student id into the dictionary with the rest of all the items from the api response
                sections.append({**s, "Student Id": player_id})  # copy + inject id

    # Create the dataframe in one go
    df = pd.json_normalize(
        sections,
        record_path="ratingRecords",
        meta=["Student Id", "sectionName", ["event", "name"], ["event", "stateCode"], ["event", "endDate"]],
    )
    return df.rename(columns=COLUMNS)[["Student Id", *COLUMNS.values()]]


def filter_recent(df: pd.DataFrame, days: int = 7, today: date | None = None) -> pd.DataFrame:
    today = today or date.today()
    cutoff = pd.Timestamp(today - timedelta(days=days))
    end_dates = pd.to_datetime(df["Tournament End Date"])
    df = df[end_dates >= cutoff]
    return df
