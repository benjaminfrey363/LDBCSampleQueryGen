
# QUERY 6: Tag co-occurrence

# Given a start Person with ID $personId and a Tag with name $tagName, find the other Tags that
# occur together with this Tag on Posts that were created by start Person’s friends and friends of
# friends (excluding start Person). Return top 10 Tags, and the count of Posts that were created by
# these Persons, which contain both this Tag and the given Tag.

# Params for query:
#   1. $personId - randomly chosen start person
#   2. $tagName - randomly chosen tag from posts of friends/friends of friends of start person

# RELAXED TO JUST CHOOSE A RANDOM TAGS, DOES NOT GUARANTEE CO-OCCURRENCE

import pandas as pd
import random
import os

def generate_query6_parameters(csv_dir: str, output_file: str, num_samples: int = 10):
    # Read data with correct delimiter
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|")
    tag_df = pd.read_csv(os.path.join(csv_dir, "static__Tag.csv"), sep="|")

    # Rename for easier use
    person_df.rename(columns={"id": "personId"}, inplace=True)
    tag_df.rename(columns={"name": "tagName"}, inplace=True)

    # Drop nulls just in case
    person_df = person_df.dropna(subset=["personId"])
    tag_df = tag_df.dropna(subset=["tagName"])

    # Prepare output list
    params = []

    # Ensure we have enough data to sample
    if len(person_df) == 0 or len(tag_df) == 0:
        print("Empty person or tag data.")
        return

    for _ in range(num_samples):
        person_id = person_df.sample(1)["personId"].values[0]
        tag_name = tag_df.sample(1)["tagName"].values[0]
        params.append((person_id, tag_name))

    # Write to CSV
    out_df = pd.DataFrame(params, columns=["personId", "tagName"])
    out_df.to_csv(output_file, index=False)
    print(f"Wrote {len(out_df)} relaxed Query 6 parameter rows to {output_file}")

if __name__ == "__main__":
    generate_query6_parameters(
        csv_dir="../flat_csv", 
        output_file="query6_parameters.csv", 
        num_samples=10
    )

