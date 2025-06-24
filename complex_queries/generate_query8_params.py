
# QUERY 8: Recent replies

# Given a start Person with ID $personId, find the most recent Comments that are replies to Messages
# of the start Person. Only consider direct (single-hop) replies, not the transitive (multi-hop) ones.
# Return the reply Comments, and the Person that created each reply Comment.

# Params for query:
#   1. $personID - just randomly chosen personID. that's it for this one!

import pandas as pd
import os
import random

def generate_query8_parameters(csv_dir: str, output_file: str, num_samples: int = 10):
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|")

    # Just get person IDs
    person_ids = person_df["id"].dropna().unique()

    # Sample randomly
    selected_ids = random.sample(list(person_ids), min(num_samples, len(person_ids)))

    out_df = pd.DataFrame(selected_ids, columns=["personId"])
    out_df.to_csv(output_file, index=False)
    print(f"Wrote {len(out_df)} Query 8 parameters to {output_file}")

if __name__ == "__main__":
    generate_query8_parameters(
        csv_dir="../flat_csv",
        output_file="query8_parameters.csv",
        num_samples=10
    )
