
# QUERY 12: Expert search

# Given a start Person with ID $personId, find the Comments that this Person’s friends made in reply
# to Posts, considering only those Comments that are direct (single-hop) replies to Posts, not the
# transitive (multi-hop) ones. Only consider Posts with a Tag in a given TagClass with name $tagClassName or in a descendent of that TagClass. Count the number of these reply Comments, and
# collect the Tags that were attached to the Posts they replied to, but only collect Tags with the given
# TagClass or with a descendant of that TagClass. Return Persons with at least one reply, the reply
# count, and the collection of Tags.

# params for query:
#   1. $personId - randomly chosen person ID
#   2. $tagClassName - randomly chosen tag class

import pandas as pd
import os
import random

def generate_query12_parameters(csv_dir: str, output_file: str, num_samples: int = 10):
    # Load person IDs
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|")
    person_ids = person_df["id"].dropna().unique()

    # Load tag class names
    tagclass_df = pd.read_csv(os.path.join(csv_dir, "static__TagClass.csv"), sep="|")
    tag_class_names = tagclass_df["name"].dropna().unique()

    # Generate parameter rows
    params = []
    for _ in range(num_samples):
        person_id = random.choice(person_ids)
        tag_class_name = random.choice(tag_class_names)
        params.append({
            "personId": person_id,
            "tagClassName": tag_class_name
        })

    # Write to CSV
    out_df = pd.DataFrame(params)
    out_df.to_csv(output_file, index=False)
    print(f"Wrote {len(out_df)} Query 12 parameters to {output_file}")

if __name__ == "__main__":
    generate_query12_parameters(
        csv_dir="../flat_csv",
        output_file="query12_parameters.csv",
        num_samples=10
    )
