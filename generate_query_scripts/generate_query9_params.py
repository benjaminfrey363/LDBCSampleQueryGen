
# QUERY 9: Recent messages by friends or friends of friends

# Given a start Person with ID $personId, find the most recent Messages created by that Person’s
# friends or friends of friends (excluding the start Person). Only consider Messages created before
# the given $maxDate (excluding that day).

# params for query:
#   1. $personId - randomly chosen
#   2. $maxDate - randomly selected in range of message creation dates

import pandas as pd
import os
import random
from datetime import datetime, timedelta

def random_date(start: datetime, end: datetime) -> str:
    """Return a random date string in ISO format between start and end."""
    delta = end - start
    random_days = random.randint(1, delta.days)
    random_dt = start + timedelta(days=random_days)
    return random_dt.strftime("%Y-%m-%d")

def generate_query9_parameters(csv_dir: str, output_file: str, num_samples: int = 10):
    # Load persons
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|")
    person_ids = person_df["id"].dropna().unique()

    # Load messages (or posts) with creation dates
    message_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Post.csv"), sep="|")
    # Assume creationDate column exists and parse to datetime
    message_df["creationDate"] = pd.to_datetime(message_df["creationDate"])

    # Get global min and max dates of messages for date sampling
    min_date = message_df["creationDate"].min()
    max_date = message_df["creationDate"].max()

    # Sample persons randomly
    selected_ids = random.sample(list(person_ids), min(num_samples, len(person_ids)))

    # For each sample, pick a random maxDate between min_date and max_date - 1 day
    params = []
    for pid in selected_ids:
        # Random maxDate before max_date to avoid future dates
        max_date_sample = random_date(min_date, max_date - timedelta(days=1))
        params.append({"personId": pid, "maxDate": max_date_sample})

    # Write out parameters CSV
    out_df = pd.DataFrame(params)
    out_df.to_csv(output_file, index=False)
    print(f"Wrote {len(out_df)} Query 9 parameters to {output_file}")

if __name__ == "__main__":
    generate_query9_parameters(
        csv_dir="../flat_csv",
        output_file="query9_parameters.csv",
        num_samples=10
    )

