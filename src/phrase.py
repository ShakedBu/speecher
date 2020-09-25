from src.DBUtils import execute_query
from src.queries import LAST_PHRASE_INDEX, NEW_PHRASE_PART, SEARCH_PHRASE, GET_ALL_PHRASES


def create_new_phrase(words):
    phrase_id = execute_query(LAST_PHRASE_INDEX, True, True)[0]
    word_index = 1

    for curr_word in words:
        # Add word to phrase
        execute_query(NEW_PHRASE_PART.format(word_index, phrase_id, curr_word))
        word_index += 1


def get_phrases(speech_id, query):
    return execute_query(SEARCH_PHRASE.format(query))


def get_all_phrases():
    results = []
    phrases = {}
    phrases_words = execute_query(GET_ALL_PHRASES, True)

    for phrase_word in phrases_words:
        phrase_id = phrase_word[0]
        if phrase_id not in phrases:
            phrases[phrase_id] = {'id': phrase_id, 'text': ""}

        phrases[phrase_id]['text'] = "{} {}".format(phrases[phrase_id]['text'], phrase_word[3].strip())

    for phrase in phrases.values():
        results.append(phrase)

    return results
