import argparse
import os
from pathlib import Path

# Import all query parameter generators
from generate_query1_params import generate_query1_parameters
from generate_query2_params import generate_query2_parameters
from generate_query3_params import generate_query3_parameters
from generate_query4_params import generate_query4_parameters
from generate_query5_params import generate_query5_parameters
from generate_query6_params import generate_query6_parameters
from generate_query7_params import generate_query7_parameters
from generate_query8_params import generate_query8_parameters
from generate_query9_params import generate_query9_parameters
from generate_query10_params import generate_query10_parameters
from generate_query11_params import generate_query11_parameters
from generate_query12_params import generate_query12_parameters
from generate_query13_params import generate_query13_parameters
from generate_query14_params import generate_query14_parameters

# Mapping query number → function
QUERY_FUNCTIONS = {
    1: generate_query1_parameters,
    2: generate_query2_parameters,
    3: generate_query3_parameters,
    4: generate_query4_parameters,
    5: generate_query5_parameters,
    6: generate_query6_parameters,
    7: generate_query7_parameters,
    8: generate_query8_parameters,
    9: generate_query9_parameters,
    10: generate_query10_parameters,
    11: generate_query11_parameters,
    12: generate_query12_parameters,
    13: generate_query13_parameters,
    14: generate_query14_parameters,
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
        fn(csv_dir=flat_csv_dir, output_file=output_path, num_samples=num_queries)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LDBC SNB Interactive query parameters")
    parser.add_argument("--flat_csv_dir", type=str, required=True, help="Path to flat CSV directory")
    parser.add_argument("--output_dir", type=str, required=True, help="Where to write parameter CSVs")
    parser.add_argument("--queries", type=str, help='Which queries to run (e.g., "1-5,7"). Default is all 1-14')
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
