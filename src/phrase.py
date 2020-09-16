from src.DBUtils import execute_query
from src.queries import LAST_PHRASE_INDEX, NEW_PHRASE_PART, GET_WORD, SEARCH_PHRASE


def create_new_phrase(words):
    phrase_id = execute_query(LAST_PHRASE_INDEX, True, True)
    word_index = 1

    for curr_word in words:
        # Get word
        word = execute_query(GET_WORD.format(curr_word), True, True)

        # Add word to phrase
        execute_query(NEW_PHRASE_PART.format(word_index, phrase_id[0], word[0]))
        word_index += 1


def get_phrases(speech_id, query):
    return execute_query(SEARCH_PHRASE.format(query))
