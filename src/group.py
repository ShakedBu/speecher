from src.DBUtils import execute_query
from .queries import NEW_GROUP, GET_WORD, ADD_WORD_TO_GROUP, SEARCH_GROUP, GET_GROUP, DELETE_WORD_FROM_GROUP, \
    ADD_WORD_TO_GROUP, GET_ALL_GROUPS


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
    if query != "":
        return execute_query(SEARCH_GROUP.format(query))
    return execute_query(GET_ALL_GROUPS, True)


def get_group(group_id):
    return execute_query(GET_GROUP.format(group_id))


def add_words_to_group(group_id, words):
    for word in words:
        execute_query(ADD_WORD_TO_GROUP.format(group_id, word))


def remove_words_from_group(group_id, words):
    for word in words:
        execute_query(DELETE_WORD_FROM_GROUP.format(group_id, word))
