from src.DBUtils import execute_query
from src.queries import NEW_GROUP, GET_WORD, ADD_WORD_TO_GROUP, SEARCH_GROUP


def create_new_group(name, words):
    group = execute_query((NEW_GROUP, name), True, True)
    group_id = group[0]

    # Add words to group
    for curr_word in words:
        # Get word
        word = execute_query((GET_WORD, curr_word), True, True)

        # Add to group
        execute_query((ADD_WORD_TO_GROUP, (group_id, word[0])))


def get_groups(query):
    return execute_query((SEARCH_GROUP, query))
