# LDBCSampleQueryGen

Python scripts to generate parameter CSV files for LDBC SNB Interactive workload complex queries 1-14, and simple queries 1-7. Individual parameter generation functions for each query, as well as a wrapper to generate full or partial query workloads, and a script flatten_ldbc_csvs.py to convert the default generated output of ldbc_snb_datagen to a human (and script)-readable directory.

# Overview

# Complex queries

Each query parameter generator script complex_queries/generate_query(n)_params.py produces randomized parameter sets based on a graph db directory taken as input.

# Simple queries

Functions to generate parameters for simple queries are contained in simple_queries.py, each simply taking the number of desired queries as argument. Default CSV directory and output directories are declared as constants, but can be modified in the script if desired.

Query parameters are constructed in accordance with LDBC SNB documentation: https://ldbcouncil.org/ldbc_snb_docs/workload-interactive-v2.pdf in some cases the parameter generation is simplified to reduce computation time, and as these queries are intended for testing. For example, in some queries we do not validate the expected output - for complex query 13, LDBC has two variants of the query - one which guarantees that no path exists between the two $personId parameters, and the other guarantees a 4-hop path. For our purposes, we do no such validation and do not guarantee the expected output of the query. These inconsistencies are documented in the script for each query.

All scripts expect a flattened CSV dataset directory, which can be obtained by calling the script flatten_ldbc_csvs.py on the default output directory generated by the LDBC SNB data generator (https://github.com/ldbc/ldbc_snb_datagen_spark).

Generated query parameters are saved to generate_query_scripts/params.

# Requirements

Python 3.7+, pandas

# Usage

Before generating queries, flatten_ldbc_csvs.py expects passed database to be in the default form of output from ldbc_snb_datagen (directory "out" constructed by the data generator).

If output directory from ldbc_snb_datagen is placed in the root of this repository without renaming, running flatten_ldbc_csvs.py with no arguments will by default reformat into flattened csv data (directory flat_csv) which can then be interpreted by our scripts. Expected directory name can be changed in this script.

# Complex Queries

To generate all queries (in complex_queries directory):

    python generate_queries_wrapper.py --flat_csv_dir </path/to/flat_csv> --output_dir <./params> --num_queries <n>

A subset of queries to generate can be specified using --queries, specifying the desired range as a range - e.g. "1-5,7,10-11":

    python generate_queries_wrapper.py --flat_csv_dir </path/to/flat_csv> --output_dir <./params> --queries <1-5,7,10-11> --num_queries <n>

# Simple Queries

Same argument specification as for complex queries, but call from root directory.
To generate all simple queries:

    python simple_queries_wrapper.py --flat_csv_dir </path/to/flat_csv> --output_dir <path/to/outputdirectory> --num_queries <n>

And again, a subset of queries to generate can be specified using --queries and a specified range. For example, to only geneate query parameters 1-3 and 6, can specifiy

    python simple_queries_wrapper.py --flat_csv_dir </path/to/flat_csv> --output_dir <path/to/outputdirectory> --queries 1-3,6 --num_queries <n>

# Example datasets

Example generated queries currently populate the generate_query_scripts/params directory, generated using n=100 on a scale factor 0.01 database, the output of ldbc_snb_datagen.

This database can be found in the following public google drive folder for reference:

https://drive.google.com/drive/folders/1EOrcDWx3MGUgkLnf-UStntcMwuzYJaq2?usp=sharing

