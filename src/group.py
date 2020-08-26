from src.DBUtils import execute_query
from src.queries import NEW_GROUP, GET_WORD, ADD_WORD_TO_GROUP, SEARCH_GROUP, GET_GROUP


def create_new_group(name, words):
    group = execute_query(NEW_GROUP.format(name), True, True)
    group_id = group[0]

    # Add words to group
    for curr_word in words:
        # Get word
        word = execute_query(GET_WORD.format(curr_word), True, True)

        # Add to group
        execute_query(ADD_WORD_TO_GROUP.format(group_id, word[0]))


def search_groups(query):
    return execute_query(SEARCH_GROUP.format(query))


def get_group(group_id):
    return execute_query(GET_GROUP.format(group_id))
