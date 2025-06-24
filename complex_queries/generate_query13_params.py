
# QUERY 13: Single shortest path

# Given two Persons with IDs $person1Id and $person2Id, find the shortest path between these two
# Persons in the subgraph induced by the knows edges.
# Variants in specific documentation where queries are produced guaranteeing
# that either a) no path exists or b) 4-hop path exists and is shortest
# for our test queries, we won't worry about this and just pick two distinct random people

# params for query:
#   1. $person1Id - randomly chosen person ID
#   2. $person2Id - randomly chosen distinct person ID

import pandas as pd
import os
import random

def generate_query13_parameters(csv_dir: str, output_file: str, num_samples: int = 10):
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
    print(f"Wrote {len(out_df)} Query 13 parameters to {output_file}")

if __name__ == "__main__":
    generate_query13_parameters(
        csv_dir="../flat_csv",
        output_file="query13_parameters.csv",
        num_samples=10
    )

