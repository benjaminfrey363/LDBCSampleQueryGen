
from sample import *

CSV_DIR = "flat_csv"
OUTPUT_DIR = "queries"


##################################
## LDBC SIMPLE QUERY GENERATION ##
##################################


# ALL QUERIES RETURNED AS LIST OF OF DICTIONARIES, EACH DICTIONARY REPRESENTING A
# QUERY (dictionary of parameters).
# These list dictionaries are then cast to writable strings and can be written to
# a CSV by wrapper functions

# NOTE: based on LDBC documentation, a "message" is defined to be either a post or a comment


# QUERY 1: Profile of a person
# 
# Given a start Person with ID $personId, retrieve their first name, last name, birthday, IP address,
# browser, and city of residence.
# 
# Queries of form personId: <$personId>
def generate_simple_query1 ( num_queries: int, csv_dir: str = CSV_DIR ):
    # generate num_queries random $personIds
    personIds = simple_sample (CSV_DIR, "Person", "id", num_queries, 1)
    # format queries and return
    queries = format_query_list ( ["personId"] , [personIds] )
    return queries


# QUERY 2: Recent messages of a person
#
# Given a start Person with ID $personId, retrieve the last 10 Messages created by that user. For each
# Message, return that Message, the original Post in its conversation (post), and the author of that Post
# (originalPoster). If any of the Messages is a Post, then the original Post (post) will be the same
# Message, i.e. that Message will appear twice in that result.
#
# Queries of form personId: <$personId>
def generate_simple_query2 ( num_queries: int, csv_dir: str = CSV_DIR ):
    # same as query 1, just generate num_queries random $personIds
    personIds = simple_sample ( CSV_DIR, "Person", "id", num_queries, 1 )
    # format queries and return
    queries = format_query_list ( ["personId"] , [personIds] )
    return queries


# QUERY 3: Friends of a person
#
# Given a start Person with ID $personId, retrieve all of their friends, and the date at which they
# became friends.
#
# Queries of form personId: <$personId>
def generate_simple_query3 ( num_queries: int, csv_dir: str = CSV_DIR ):
    # same as queries 1 and 2, just generate num_queries random $personIds
    personIds = simple_sample ( CSV_DIR, "Person", "id", num_queries, 1 )
    # format queries and return
    queries = format_query_list ( ["personId"] , [personIds] )
    return queries


# QUERY 4: Content of a message
#
# Given a Message with ID $messageId, retrieve its content and creation date.
#
# Queries of form messageId: <$messageId>
def generate_simple_query4 ( num_queries: int, csv_dir: str = CSV_DIR ):
    # generate num_queries random $messageIds - either the IDs of posts or comments
    messageIds = simple_sample_multifile ( CSV_DIR, ["Comment", "Post"], ["id", "id"], num_queries, 1 )
    # format queries and return
    queries = format_query_list ( ["messageId"] , [messageIds] )
    return queries


# QUERY 5: Creator of a message
#
# Given a Message with ID $messageId, retrieve its author.
#
# Queries of form messageId: <$messageId>
def generate_simple_query5 ( num_queries: int, csv_dir: str = CSV_DIR ):
    # generate num_queries random $messageIds - either the IDs of posts or comments
    messageIds = simple_sample_multifile ( CSV_DIR, ["Comment", "Post"], ["id", "id"], num_queries, 1 )
    # format queries and return
    queries = format_query_list ( ["messageId"] , [messageIds] )
    return queries


# QUERY 6: Forum of a message
#
# Given a Message with ID $messageId, retrieve the Forum that contains it and the Person that moderates that Forum. Since Comments are not directly contained in Forums, for Comments, return the
# Forum containing the original Post in the thread which the Comment is replying to.
#
# Queries of form messageId: <$messageId>
def generate_simple_query6 ( num_queries: int, csv_dir: str = CSV_DIR ):
    # generate num_queries random $messageIds - either the IDs of posts or comments
    messageIds = simple_sample_multifile ( CSV_DIR, ["Comment", "Post"], ["id", "id"], num_queries, 1 )
    # format queries and return
    queries = format_query_list ( ["messageId"] , [messageIds] )
    return queries


# QUERY 7: Replies of a message
#
# Given a Message with ID $messageId, retrieve the (1-hop) Comments that reply to it.
# In addition, return a boolean flag knows indicating if the author of the reply (replyAuthor) knows
# the author of the original message (messageAuthor). If author is same as original author, return
# False for knows flag.
#
# Queries of form messageId: <$messageId>
def generate_simple_query7 ( num_queries: int, csv_dir: str = CSV_DIR ):
    # generate num_queries random $messageIds - either the IDs of posts or comments
    messageIds = simple_sample_multifile ( CSV_DIR, ["Comment", "Post"], ["id", "id"], num_queries, 1 )
    # format queries and return
    queries = format_query_list ( ["messageId"] , [messageIds] )
    return queries

