
# Helper functions for sampling csvs to generate query parameters

import pandas as pd
import os
import random
from typing import List

dynamic_sampleable = ["Comment", "Forum", "Person", "Post"]
static_sampleable = ["Organisation", "Place", "Tag", "TagClass"]


#############################################################################
# functions for simpling sampling of single non-constrained entry from file #
#############################################################################

# Given a specified csv_dir, node file and type, return list of unique type entries in node file
def get_deduplicated_list ( 
    csv_dir: str = "flat_csv", 
    file: str = "Person",
    type: str = "firstName"
):
    # check for invalid file arg
    if file not in (dynamic_sampleable + static_sampleable):
        print("Passed invalid type argument to get_deduplicated_list(). Returning empty list...")
        return []
    # otherwise open file
    df = None
    if file in dynamic_sampleable:
        df = pd.read_csv(os.path.join(csv_dir, "dynamic__" + file + ".csv"), sep="|")
    else:
        df = pd.read_csv(os.path.join(csv_dir, "static__" + file + ".csv"), sep="|")
    if df.empty:
        print("Failed to read specified file in get_deduplicated_list(). Returning empty list...")
        return []
    # check for specified type in df
    if type not in df.columns:
        print("Could not find specified type in dataframe passed to get_deduplicated_list(). Returning empty list...")
        return []
    # else, found type and we can sample.
    unique_entries = df[type].dropna().unique() # deduplicate
    return list(unique_entries)


# Simply sample num_sample non-constrained entries of specified type from specified file in csv_dir.
# k optionally allows for sampling distinct k-tuples, returning num_samples k-tuples with no dups instead
def simple_sample ( 
    csv_dir: str = "flat_csv",
    file: str = "Person",
    type: str = "firstName",
    num_samples: int = 10,
    k: int = 1
):
    samples = []
    # get deduplicated list of entries of specified type in specified file
    unique_list = get_deduplicated_list ( csv_dir , file , type )
    # check for empty return value
    if len(unique_list) == 0:
        print("Empty list returned by get_deduplicated_list(). Returning empty sample from simple_sample().")
        return samples
    # else, randomly sample and return
    for _ in range(0,num_samples):
        samples.append(random.sample(unique_list, k))
    if k > 1:
        return samples
    else:
        # flatten for k = 1
        return [sample[0] for sample in samples]


# Simply sample num_sample non-constrained entries of specified type(s) from specified file(s) in csv_dir.
# That is, we join specified values together and sample from this shared pool.
# k optionally allows for sampling distinct k-tuples, returning num_samples k-tuples with no dups instead
# default args are those used for "message" sampling
def simple_sample_multifile (
        csv_dir: str = "flat_csv",
        files: List[str] = ["Comment", "Post"],
        types: List[str] = ["id", "id"],
        num_samples: int = 10,
        k: int = 1
):
    samples = []
    if len(files) != len(types):
        print("Passed invalid arguments to simple_sample_multifile(). Must specify the same number of files and types. Returning empty list from simple_sample_multifile()...")
        return samples
    # create pooled list of values of each type from each file
    pooled_list = []
    for i in range(0, len(files)):
        pooled_list += get_deduplicated_list ( csv_dir , files[i] , types[i] )
    # check for empty list
    if len(pooled_list) == 0:
        print("Empty list returned by get_deduplicated_list(). Returning empty sample from simple_sample().")
        return samples
    # randomly sample from pooled list and return
    for _ in range(0,num_samples):
        samples.append(random.sample(pooled_list, k))
    if k > 1:
        return samples
    else:
        # flatten for k = 1
        return [sample[0] for sample in samples]


####################################################
# Functions for constructing maps and edge lookups #
####################################################


# Conduct edge lookup.
# In edge_file, find all entries with input_type = input_value.
# Return list of all output_type values of these entries ("adjacent nodes")
def edge_lookup (
    csv_dir: str = "flat_csv",
    edge_file: str = "Person_knows_Person",
    input_type: str = "Person1Id",
    output_type: str = "Person2Id",
    input_value: str = "332"
):
    # try to read file
    df = pd.read_csv(os.path.join(csv_dir, "dynamic__" + edge_file + ".csv"), sep="|")
    if df.empty:
        print("Failed to read specified file in edge_lookup(). Returning empty list...")
        return []
    # check for specified types
    if input_type not in df.columns or output_type not in df.columns:
        print("Could not find specified types in dataframe passed to edge_lookup(). Returning empty list...")
        return []
    # otherwise, conduct lookup and return list
    matches = df[df[input_type] == input_value][output_type].dropna().unique()
    return list(matches)


######################################
# Functions for formatting query CSV #
######################################

"""
Format a list of queries from a list of parameter names and a matrix of values.

Args:
    param_list (List[str]): List of parameter names (e.g., ["startDate", "endDate", "tagId"]).
    val_matrix (List[List[Any]]): 2D list where val_matrix[i][j] is the jth parameter of the ith query.

Returns:
    List[Dict[str, Any]]: A list of queries formatted as dictionaries.
"""
def format_query_list ( param_list , val_matrix ):
    rows = []
    num_queries = len(val_matrix[0])
    for i in range(0, num_queries):
        # construct query
        query = {}
        for j, param in enumerate(param_list):
            query[param] = val_matrix[j][i]
        rows.append(query)
    return rows


