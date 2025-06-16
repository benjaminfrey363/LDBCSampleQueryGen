
# QUERY 1: Transitive friends with certain name

# Given a start Person with ID $personId, find Persons with a given first name ($firstName) that the
# start Person is connected to (excluding start Person) by at most 3 steps via the knows relationships.
# Return Persons, including the distance (1..3), summaries of the Persons workplaces and places of
# study

# Params for query: 
#   1. $personID - no constraints
#   2. $firstName - no constraints

# Since no constraints, we just randomly select a personID and firstName
# for each query, and make num_queries of these queries

import pandas as pd
import random
import os

def generate_query1_parameters(csv_dir, output_file, num_samples=10):
    person_csv = os.path.join(csv_dir, "dynamic__Person.csv")

    # Load the person CSV
    df = pd.read_csv(person_csv, sep="|", usecols=["id", "firstName"])
    df = df.dropna(subset=["id", "firstName"])

    # Get unique person IDs and first names
    person_ids = df["id"].unique()
    first_names = df["firstName"].unique()

    # Generate random parameter combinations
    rows = []
    for _ in range(num_samples):
        person_id = random.choice(person_ids)
        first_name = random.choice(first_names)
        rows.append({"personId": person_id, "firstName": first_name})

    # Write to CSV
    pd.DataFrame(rows).to_csv(output_file, index=False)
    print(f"Wrote {len(rows)} query1 parameter rows to {output_file}")
