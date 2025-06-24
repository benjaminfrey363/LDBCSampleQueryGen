
# QUERY 4: New topics

# Given a start Person with ID $personId, find Tags that are attached to Posts that were created by that
# Person’s friends. Only include Tags that were attached to friends’ Posts created within a given time
# interval [$startDate, $startDate + $durationDays) (closed-open) and that were never attached
# to friends’ Posts created before this interval.

# Params for query:
#   1. $personId - randomly chosen person
#   2. $startDate - randomly chosen within bounds of post by persons friends
#   3. $durationDays - randomly chosen integer

import pandas as pd
import os
import random

def generate_query4_parameters(csv_dir, output_file, num_samples=10):
    # Load data
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|", usecols=["id"])
    knows_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person_knows_Person.csv"), sep="|")
    post_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Post.csv"), sep="|", usecols=["id", "creationDate", "CreatorPersonId"])

    # Build person → set of friends
    friends_dict = {}
    for _, row in knows_df.iterrows():
        p1, p2 = row["Person1Id"], row["Person2Id"]
        friends_dict.setdefault(p1, set()).add(p2)
        friends_dict.setdefault(p2, set()).add(p1)

    # Prepare mapping: person → post dates
    post_df["creationDate"] = pd.to_datetime(post_df["creationDate"], errors="coerce")
    person_posts = post_df.groupby("CreatorPersonId")["creationDate"].apply(list).to_dict()

    results = []
    attempts = 0
    max_attempts = num_samples * 5

    while len(results) < num_samples and attempts < max_attempts:
        attempts += 1
        person_id = random.choice(person_df["id"].tolist())

        friends = friends_dict.get(person_id, [])
        if not friends:
            continue

        # Gather all post timestamps from friends
        friend_post_dates = []
        for friend_id in friends:
            friend_post_dates.extend(person_posts.get(friend_id, []))

        if not friend_post_dates:
            continue

        friend_post_dates = pd.Series(friend_post_dates).dropna()
        if len(friend_post_dates) == 0:
            continue

        start_date = friend_post_dates.sample(1).iloc[0].normalize()
        duration_days = random.randint(10, 30)

        results.append({
            "personId": person_id,
            "startDate": start_date.isoformat(),
            "durationDays": duration_days
        })

    pd.DataFrame(results).to_csv(output_file, index=False)
    print(f"Wrote {len(results)} query4 parameter rows to {output_file}")

if __name__ == "__main__":
    generate_query4_parameters(csv_dir="../flat_csv", output_file="query4_parameters.csv", num_samples=10)

