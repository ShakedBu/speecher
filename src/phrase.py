from src.DBUtils import execute_query
from src.queries import LAST_PHRASE_INDEX, NEW_PHRASE_PART, GET_ALL_PHRASES, GET_PHRASE, GET_PARTIAL_SENTENCE, \
    SEARCH_PHRASE_FIRST, SEARCH_PHRASE_MIDDLE, SEARCH_PHRASE_LAST


def create_new_phrase(words):
    phrase_id = execute_query(LAST_PHRASE_INDEX, True, True)[0]
    word_index = 1

    for curr_word in words:
        # Add word to phrase
        execute_query(NEW_PHRASE_PART.format(word_index, phrase_id, curr_word))
        word_index += 1


def get_phrases(speech_id, phrase_id):
    results = []
    words = get_phrase(phrase_id)
    query = ""

    # Build this massive query to find all the occurrences of the phrase in the speech :)
    for word in words:
        index = word['index']
        previous_index = int(index) - 1
        word_id = word['word']

        if index == 1:
            query = SEARCH_PHRASE_FIRST.format(speech_id, word_id, '{}', index=index)
        elif index == len(words):
            last_query = SEARCH_PHRASE_LAST.format(speech_id, word_id, index=index, previous_index=previous_index)
            query = query.format(last_query)
        else:
            mid_query = SEARCH_PHRASE_MIDDLE.format(speech_id, word_id, '{}', index=index,
                                                    previous_index=previous_index)
            query = query.format(mid_query)

    phrase_appearances = execute_query(query, True)

    for appearance in phrase_appearances:
        words_in_sentence = execute_query(GET_PARTIAL_SENTENCE.format(speech_id, appearance[0], appearance[1],
                                                                      appearance[2], range=len(words)),
                                          True)
        some_sentence = ""

        # Build the sentence
        for curr_word in words_in_sentence:
            some_sentence = "{} {}".format(some_sentence, curr_word[0].strip())

        results.append({'paragraph': appearance[0], 'sentence': appearance[1], 'index': appearance[2],
                        'some_sentence': '...' + some_sentence + '...'})

    return results


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


def get_phrase(phrase_id):
    results = []
    phrase_words = execute_query(GET_PHRASE.format(phrase_id), True)

    for phrase_word in phrase_words:
        results.append({'index': phrase_word[0], 'word': phrase_word[1]})

    return results
