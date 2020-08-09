from src.DBUtils import execute_query
from src.queries import LAST_GROUP_INDEX, NEW_GROUP, FIND_WORD, ADD_WORD_TO_GROUP


def create_new_group(name, words):
    group_id = execute_query(LAST_GROUP_INDEX, True)
    execute_query((NEW_GROUP, (group_id, name)), True)

    # Add words to group
    for curr_word in words:
        # Get word
        word = execute_query((FIND_WORD, curr_word), True)

        # Add to group
        execute_query((ADD_WORD_TO_GROUP, (group_id, word[0])), True)
