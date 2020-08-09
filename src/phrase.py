from src.DBUtils import execute_query
from src.queries import LAST_PHRASE_INDEX, NEW_PHRASE_PART, FIND_WORD


def create_new_phrase(words):
    phrase_id = execute_query(LAST_PHRASE_INDEX, True)
    word_index = 1

    for curr_word in words:
        # Get word
        word = execute_query((FIND_WORD, curr_word), True)

        # Add word to phease
        execute_query((NEW_PHRASE_PART, (word_index, phrase_id[0], word[0])), True)
        word_index += 1
