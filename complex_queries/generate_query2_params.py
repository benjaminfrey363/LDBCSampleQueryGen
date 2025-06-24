
# QUERY 2: Recent messages by your friends

# Given a start Person with ID $personId, find the most recent Messages from all of that Person’s
# friends (friend nodes). Only consider Messages created before the given $maxDate (excluding that
# day).

# Params for query: 
#   1. $personID - no constraints
#   2. $maxDate - selected randomly from meaningful period - between earliest and latest messages

import pandas as pd
import random
from datetime import timedelta
import os

def generate_query2_parameters(csv_dir, output_file, num_samples=10):
    # Load necessary CSVs
    person_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person.csv"), sep="|")
    knows_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Person_knows_Person.csv"), sep="|")
    post_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Post.csv"), sep="|", usecols=["id", "CreatorPersonId", "creationDate"])
    comment_df = pd.read_csv(os.path.join(csv_dir, "dynamic__Comment.csv"), sep="|", usecols=["id", "CreatorPersonId", "creationDate"])

    # Combine Post and Comment into one messages DataFrame
    post_df["creatorId"] = post_df["CreatorPersonId"]
    comment_df["creatorId"] = comment_df["CreatorPersonId"]

    post_df["creationDate"] = pd.to_datetime(post_df["creationDate"], errors="coerce")
    comment_df["creationDate"] = pd.to_datetime(comment_df["creationDate"], errors="coerce")

    messages_df = pd.concat([
        post_df[["creatorId", "creationDate"]],
        comment_df[["creatorId", "creationDate"]]
    ]).dropna()

    query_rows = []
    attempts = 0
    max_attempts = num_samples * 10

    while len(query_rows) < num_samples and attempts < max_attempts:
        attempts += 1
        person = person_df.sample(1).iloc[0]
        person_id = person["id"]

        # Undirected edge: get friends
        friends = knows_df[knows_df["Person1Id"] == person_id]["Person2Id"].tolist()
        friends += knows_df[knows_df["Person2Id"] == person_id]["Person1Id"].tolist()

        if not friends:
            continue

        friend_messages = messages_df[messages_df["creatorId"].isin(friends)]
        if len(friend_messages) < 2:
            continue

        friend_messages = friend_messages.sort_values("creationDate")
        earliest = friend_messages["creationDate"].min()
        latest = friend_messages["creationDate"].max()

        if (latest - earliest).days < 2:
            continue

        offset_days = random.randint(1, (latest - earliest).days - 1)
        max_date = earliest + timedelta(days=offset_days)

        query_rows.append({
            "personId": person_id,
            "maxDate": max_date.isoformat(),
            "limit": 20
        })

    if not query_rows:
        print("No suitable parameters found.")
        return

    pd.DataFrame(query_rows).to_csv(output_file, index=False)
    print(f"Wrote {len(query_rows)} query2 parameter rows to {output_file}")

