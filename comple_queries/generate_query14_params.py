
# QUERY 14: Trusted connection paths (v2)

# This query is used in SNB Interactive v2.
# Find a cheapest path between two given Persons with IDs $person1Id and $person2Id in the interaction subgraph. If there are multiple cheapest paths, any of them can be returned. Do not
# return any rows if there is no path between the Persons.

# as with query 13, there are variants of this query in the official documentation
# one guarantees there is no path, the other that there is a 4-hop path.
# for our testing purposes, just randomly produce two distinct people.

import pandas as pd
import os
import random

def generate_query14_parameters(csv_dir: str, output_file: str, num_samples: int = 10):
    # Load person IDs
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|")
    person_ids = person_df["id"].dropna().unique()

    # Generate random distinct pairs
    params = []
    for _ in range(num_samples):
        person1, person2 = random.sample(list(person_ids), 2)
        params.append({
            "person1Id": person1,
            "person2Id": person2
        })

    # Write to CSV
    out_df = pd.DataFrame(params)
    out_df.to_csv(output_file, index=False)
    print(f"Wrote {len(out_df)} Query 14 parameters to {output_file}")

if __name__ == "__main__":
    generate_query14_parameters(
        csv_dir="../flat_csv",
        output_file="query14_parameters.csv",
        num_samples=10
    )
