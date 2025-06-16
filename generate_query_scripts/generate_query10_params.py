
# QUERY 10: Friend recommendation

# Given a start Person with ID $personId, find that Person’s friends of friends (foaf) – excluding the
# start Person and his/her immediate friends –, who were born on or after the 21st of a given $month
# (in any year) and before the 22nd of the following month.

# params for query:
#   1. $personID - randomly chosen
#   2. $month - randomly chosen month between 1 and 12

import pandas as pd
import os
import random

def generate_query10_parameters(csv_dir: str, output_file: str, num_samples: int = 10):
    # Load persons
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|")
    person_ids = person_df["id"].dropna().unique()

    # Randomly sample person IDs
    selected_ids = random.sample(list(person_ids), min(num_samples, len(person_ids)))

    # Generate (personId, month) pairs
    params = []
    for pid in selected_ids:
        month = random.randint(1, 12)
        params.append({"personId": pid, "month": month})

    # Write to CSV
    out_df = pd.DataFrame(params)
    out_df.to_csv(output_file, index=False)
    print(f"Wrote {len(out_df)} Query 10 parameters to {output_file}")

if __name__ == "__main__":
    generate_query10_parameters(
        csv_dir="../flat_csv",
        output_file="query10_parameters.csv",
        num_samples=10
    )
