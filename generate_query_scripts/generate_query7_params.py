
# QUERY 7: Recent Likers

# Given a start Person with ID $personId, find the most recent likes on any of start Person’s Messages. Find Persons that liked (likes edge) any of start Person’s Messages, the Messages they liked
# most recently, the creation date of that like, and the latency in minutes (minutesLatency) between
# creation of Messages and like. Additionally, for each Person found return a flag indicating (isNew)
# whether the liker is a friend of start Person. In case that a Person liked multiple Messages at the
# same time, return the Message with lowest identifier.

# Params for query:
#   1. $personID - just randomly chosen personID. that's it for this one!

import pandas as pd
import os
import random

def generate_query7_parameters(csv_dir: str, output_file: str, num_samples: int = 10):
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|")

    # Just get person IDs
    person_ids = person_df["id"].dropna().unique()

    # Sample randomly
    selected_ids = random.sample(list(person_ids), min(num_samples, len(person_ids)))

    out_df = pd.DataFrame(selected_ids, columns=["personId"])
    out_df.to_csv(output_file, index=False)
    print(f"Wrote {len(out_df)} Query 7 parameters to {output_file}")

if __name__ == "__main__":
    generate_query7_parameters(
        csv_dir="../flat_csv",
        output_file="query7_parameters.csv",
        num_samples=10
    )

