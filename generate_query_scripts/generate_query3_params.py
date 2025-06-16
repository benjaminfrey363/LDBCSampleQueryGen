
# QUERY 3: Friends and friends of friends that have been to given countries

# Given a start Person with ID $personId, find Persons that are their friends and friends of friends
# (excluding the start Person) that have made Posts / Comments in both of the given Countries (named
# $countryXName and $countryYName), within [$startDate, $startDate + $durationDays) (closedopen interval). Only Persons that are foreign to these Countries are considered, that is Persons
# whose location Country is neither named $countryXName nor $countryYName.

# Params for query: 
#   1. $countryXName and $countryYName - distinct countries chosen randomly at beginning 
#   2. $startDate - chosen randomly in datasets time range
#   3. $durationDays - randomly chosen integer in reasonable bounds
#   4. $personID - person randomly chosen whose location is neither $countryXName or $countryYName

# NOTE: Not implemented correlated/anti-correlated country selection as in LDBC documentation

import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_query3_parameters(csv_dir, output_file, num_samples=10):
    # Load required data
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|", usecols=["id", "LocationCityId"])
    place_df = pd.read_csv(os.path.join(csv_dir, "static__Place.csv"), sep="|", usecols=["id", "name", "type", "PartOfPlaceId"])
    post_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Post.csv"), sep="|", usecols=["creationDate"])
    comment_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Comment.csv"), sep="|", usecols=["creationDate"])

    # Build mapping: place_id → (name, type, PartOfPlaceId)
    place_info = place_df.set_index("id")[["name", "type", "PartOfPlaceId"]].to_dict(orient="index")

    def get_country(place_id):
        """Walk up place hierarchy to find country name."""
        visited = set()
        while place_id is not None and place_id not in visited:
            visited.add(place_id)
            place = place_info.get(place_id)
            if place is None:
                return None
            if place["type"] == "Country":
                return place["name"]
            place_id = place["PartOfPlaceId"]
        return None

    # Build city_id → country_name mapping
    city_to_country = {
        place_id: get_country(place_id)
        for place_id, data in place_info.items()
        if data["type"] == "City"
    }

    # Map each person to their country
    person_df["country"] = person_df["LocationCityId"].map(city_to_country)

    # Get all available country names
    available_countries = sorted(set(city_to_country.values()))
    available_countries = [c for c in available_countries if c is not None]

    # Get all available message timestamps
    all_dates = pd.to_datetime(pd.concat([
        post_df["creationDate"],
        comment_df["creationDate"]
    ]), errors="coerce").dropna()

    # Generate query parameters
    query_rows = []
    attempts = 0
    max_attempts = num_samples * 5  # Avoid infinite loops

    while len(query_rows) < num_samples and attempts < max_attempts:
        attempts += 1
        countryX, countryY = random.sample(available_countries, 2)

        # Find people not from either country
        foreign_people = person_df[
            ~person_df["country"].isin([countryX, countryY])
        ]["id"].tolist()

        if not foreign_people:
            continue

        person_id = random.choice(foreign_people)
        start_date = all_dates.sample(1).iloc[0].normalize()
        duration_days = random.randint(5, 30)

        query_rows.append({
            "personId": person_id,
            "countryXName": countryX,
            "countryYName": countryY,
            "startDate": start_date.isoformat(),
            "durationDays": duration_days
        })

    # Save to CSV
    pd.DataFrame(query_rows).to_csv(output_file, index=False)
    print(f"Wrote {len(query_rows)} query3 parameter rows to {output_file}")



# Example usage
if __name__ == "__main__":
    generate_query3_parameters(csv_dir="../flat_csv", output_file="query3_parameters.csv", num_samples=10)

