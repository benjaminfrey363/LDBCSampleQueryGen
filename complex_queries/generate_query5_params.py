
# QUERY 5: New groups

# Given a start Person with ID $personId, denote their friends and friends of friends (excluding the
# start Person) as otherPerson.
# Find Forums that any Person otherPerson became a member of after a given date ($minDate). For
# each of those Forums, count the number of Posts that were created by the Person otherPerson.

# Params for query:
#   1. $personId - randomly chosen person
#   2. $minDate - randomly chosen from join dates of other people

import pandas as pd
import os
import random

def generate_query5_parameters(csv_dir, output_file, num_samples=10):
    # Load datasets
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|", usecols=["id"])
    knows_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person_knows_Person.csv"), sep="|")
    forum_member_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Forum_hasMember_Person.csv"), sep="|")
    post_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Post.csv"), sep="|", usecols=["creationDate"])

    # Parse dates
    forum_member_df["joinDate"] = pd.to_datetime(forum_member_df["creationDate"], errors="coerce")
    post_df["creationDate"] = pd.to_datetime(post_df["creationDate"], errors="coerce")

    # Build friend map
    friends_dict = {}
    for _, row in knows_df.iterrows():
        a, b = row["Person1Id"], row["Person2Id"]
        friends_dict.setdefault(a, set()).add(b)
        friends_dict.setdefault(b, set()).add(a)

    results = []
    attempts = 0
    max_attempts = num_samples * 5

    person_ids = person_df["id"].tolist()

    while len(results) < num_samples and attempts < max_attempts:
        attempts += 1
        person_id = random.choice(person_ids)
        direct_friends = friends_dict.get(person_id, set())

        if not direct_friends:
            continue

        fof = set()
        for f in direct_friends:
            fof.update(friends_dict.get(f, set()))

        other_persons = (direct_friends | fof) - {person_id}
        if not other_persons:
            continue

        # Filter Forum Memberships by these other persons
        relevant_members = forum_member_df[forum_member_df["PersonId"].isin(other_persons)]
        if relevant_members.empty:
            continue

        # Choose a minDate from their join dates
        min_date = relevant_members["joinDate"].dropna().sample(1).iloc[0].normalize()

        results.append({
            "personId": person_id,
            "minDate": min_date.isoformat()
        })

    pd.DataFrame(results).to_csv(output_file, index=False)
    print(f"Wrote {len(results)} query5 parameter rows to {output_file}")

if __name__ == "__main__":
    generate_query5_parameters(csv_dir="../flat_csv", output_file="query5_parameters.csv", num_samples=10)

