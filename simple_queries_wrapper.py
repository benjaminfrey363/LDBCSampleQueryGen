import argparse
import os
import csv
from pathlib import Path

# Import simple query parameter generator functions
from simple_queries import *

# Mapping query number → function
QUERY_FUNCTIONS = {
    1: generate_simple_query1,
    2: generate_simple_query2,
    3: generate_simple_query3,
    4: generate_simple_query4,
    5: generate_simple_query5,
    6: generate_simple_query6,
    7: generate_simple_query7,
}

def parse_query_range(query_str):
    result = set()
    for part in query_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.update(range(start, end + 1))
        else:
            result.add(int(part))
    return sorted(result)

def main(flat_csv_dir, output_dir, num_queries, selected_queries):
    flat_csv_dir = Path(flat_csv_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for q in selected_queries:
        fn = QUERY_FUNCTIONS.get(q)
        if fn is None:
            print(f"[!] No function defined for Query {q}")
            continue
        output_path = output_dir / f"query{q}_parameters.csv"
        print(f"[+] Generating Query {q} → {output_path}")
        # call function to generate queries as dictionary list
        queries = fn(num_queries, flat_csv_dir)
        # write to requested file
        with open(output_path, "w", newline="") as csvfile:
            # format as csv
            fieldnames = queries[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()       # write column headers
            writer.writerows(queries)     # write each row



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LDBC SNB Interactive query parameters")
    parser.add_argument("--flat_csv_dir", type=str, required=True, help="Path to flat CSV directory")
    parser.add_argument("--output_dir", type=str, required=True, help="Where to write parameter CSVs")
    parser.add_argument("--queries", type=str, help='Which queries to run (e.g., "1-5,7"). Default is all 1-7')
    parser.add_argument("--num_queries", type=int, default=10, help="How many queries to generate per script")

    args = parser.parse_args()

    if args.queries:
        queries_to_run = parse_query_range(args.queries)
    else:
        queries_to_run = list(QUERY_FUNCTIONS.keys())

    main(
        flat_csv_dir=args.flat_csv_dir,
        output_dir=args.output_dir,
        num_queries=args.num_queries,
        selected_queries=queries_to_run
    )
