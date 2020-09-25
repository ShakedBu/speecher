from flask_restful import Resource
from flask import request

from src.DBUtils import execute_query
from src.queries import GET_ALL_WORDS, GET_WORD_BY_LOC, GET_SENTENCE, GET_WORD_APPEARANCES_IN_SPEECH,\
    GET_PARTIAL_SENTENCE, GET_SPEECH_WORDS


class Word(Resource):
    def get(self):
        if 'speech_id' in request.args:
            if 'paragraph' in request.args:
                return get_word_by_location(request.args['speech_id'], request.args['paragraph'],
                                            request.args['sentence'], request.args['index'])
            elif 'word' in request.args:
                return get_word_appearances_in_speech(request.args['speech_id'], request.args['word'])

            return get_all_words_in_speech(request.args['speech_id'])

        return get_all_words()


def get_all_words():
    results = []
    words = execute_query(GET_ALL_WORDS, True)

    for word in words:
        results.append({'id': word[0], 'word': word[1].strip()})

    return results


def get_word_appearances_in_speech(speech_id, word):
    results = []
    word_appearances = execute_query(GET_WORD_APPEARANCES_IN_SPEECH.format(speech_id, word), True)

    # Go over the appearances and builds the results with full details
    for appearance in word_appearances:
        close_words = execute_query(GET_PARTIAL_SENTENCE.format(speech_id, appearance[0], appearance[1], appearance[2],
                                                                range=2),
                                    True)
        some_sentence = "..."

        for word in close_words:
            some_sentence = "{} {}".format(some_sentence, word[0].strip())

        results.append({'paragraph': appearance[0], 'sentence': appearance[1], 'index': appearance[2],
                        'some_sentence': some_sentence + '...', 'word': word})

    return results


def get_word_by_location(speech_id, paragraph, sentence, index):
    word = execute_query(GET_WORD_BY_LOC.format(speech_id, paragraph, sentence, index), True, True)

    if word is not None:
        sentence_words = execute_query(GET_SENTENCE.format(speech_id, paragraph, sentence), True)
        full_sentence = ""

        # Build the sentence
        for curr_word in sentence_words:
            full_sentence = "{} {}".format(full_sentence, curr_word[0].strip())

        return {'speech_id': speech_id, 'paragraph': paragraph, 'sentence': sentence, 'index': index,
                'word': word[1].strip(), 'full_sentence': full_sentence}


def get_all_words_in_speech(speech_id):
    results = []
    words = execute_query(GET_SPEECH_WORDS.format(speech_id), True)

    for word in words:
        results.append({'id': word[0], 'word': word[1].strip()})

    return results
