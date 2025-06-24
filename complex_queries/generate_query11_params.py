
# QUERY 11: Job referral

# Given a start Person with ID $personId, find that Person’s friends and friends of friends (excluding
# start Person) who started working in some Company in a given Country with name $countryName,
# before a given date ($workFromYear).

# params for query:
#   1. $personId - randomly chosen
#   2. $countryName - randomly chosen from static__Place.csv
#   3. $workFromYear - randomly chosen in range determined by dynamic__Person_workAt_Company.csv

import pandas as pd
import os
import random

def generate_query11_parameters(csv_dir: str, output_file: str, num_samples: int = 10):
    # Load person IDs
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|")
    person_ids = person_df["id"].dropna().unique()

    # Load country names
    place_df = pd.read_csv(os.path.join(csv_dir, "static__Place.csv"), sep="|")
    country_df = place_df[place_df["type"] == "Country"]
    country_names = country_df["name"].dropna().unique()

    # Load employment data and extract years
    work_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person_workAt_Company.csv"), sep="|")
    work_years = work_df["workFrom"].dropna()
    min_year = int(work_years.min())
    max_year = int(work_years.max())

    #print(f"Work years range from {min_year} to {max_year}")

    # Generate parameter rows
    params = []
    for _ in range(num_samples):
        person_id = random.choice(person_ids)
        country_name = random.choice(country_names)
        work_year = random.randint(min_year, max_year)
        params.append({
            "personId": person_id,
            "countryName": country_name,
            "workFromYear": work_year
        })

    # Write to CSV
    out_df = pd.DataFrame(params)
    out_df.to_csv(output_file, index=False)
    print(f"Wrote {len(out_df)} Query 11 parameters to {output_file}")

if __name__ == "__main__":
    generate_query11_parameters(
        csv_dir="../flat_csv",
        output_file="query11_parameters.csv",
        num_samples=10
    )
