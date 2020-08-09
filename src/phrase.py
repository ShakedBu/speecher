from src.DBUtils import execute_query
from src.queries import LAST_PHRASE_INDEX, NEW_PHRASE_PART, GET_WORD, SEARCH_PHRASE


def create_new_phrase(words):
    phrase_id = execute_query(LAST_PHRASE_INDEX, True)
    word_index = 1

    for curr_word in words:
        # Get word
        word = execute_query((GET_WORD, curr_word), True)

        # Add word to phrase
        execute_query((NEW_PHRASE_PART, (word_index, phrase_id[0], word[0])), True)
        word_index += 1


def get_phrases(query):
    return execute_query((SEARCH_PHRASE, query))
