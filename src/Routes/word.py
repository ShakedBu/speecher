from flask_restful import Resource
from flask import request, abort
from flask_jwt import jwt_required

from src.DBUtils import execute_query_safe
from src.queries import GET_ALL_WORDS, GET_WORD_BY_LOC, GET_SENTENCE, GET_WORD_APPEARANCES_IN_SPEECH,\
    GET_PARTIAL_SENTENCE, GET_SPEECH_WORDS


class Word(Resource):
    @jwt_required()
    def get(self):
        if 'speech_id' in request.args:
            if 'paragraph' in request.args:
                return get_word_by_location(request.args['speech_id'], request.args['paragraph'],
                                            request.args.get('sentence'), request.args.get('index'))
            elif 'word' in request.args:
                return get_word_appearances_in_speech(request.args['speech_id'], request.args['word'])

            return get_all_words_in_speech(request.args['speech_id'])

        return get_all_words()


def get_all_words():
    results = []
    words = execute_query_safe(GET_ALL_WORDS, is_fetch=True)

    for word in words:
        results.append({'id': word[0], 'word': word[1].strip()})

    return results


def get_word_appearances_in_speech(speech_id, word):
    if speech_id is None or word is None:
        abort(400, 'must get speech id & word id')

    results = []
    query = '%' + word + '%'
    word_appearances = execute_query_safe(GET_WORD_APPEARANCES_IN_SPEECH, {'speech_id': speech_id, 'word': query}, True)

    if word_appearances is None or len(word_appearances) == 0:
        abort(500, 'word {} not appear in speech {}'.format(word, speech_id))

    # Go over the appearances and builds the results with full details
    for appearance in word_appearances:
        close_words = execute_query_safe(GET_PARTIAL_SENTENCE, {'speech_id': speech_id, 'paragraph': appearance[0],
                                                                'sentence': appearance[1], 'index': appearance[2],
                                                                'range': 2},
                                         True)
        some_sentence = "..."

        for word in close_words:
            some_sentence = "{} {}".format(some_sentence, word[0].strip())

        results.append({'paragraph': appearance[0], 'sentence': appearance[1], 'index': appearance[2],
                        'some_sentence': some_sentence + '...', 'word': word})

    return results


def get_word_by_location(speech_id, paragraph, sentence, index):
    if speech_id is None or paragraph is None or sentence is None or index is None:
        abort(400, 'Must get all fields for location')

    word = execute_query_safe(GET_WORD_BY_LOC, {'speech_id': speech_id, 'paragraph': paragraph,
                                                'sentence': sentence, 'index': index}, True, True)

    if word is not None:
        sentence_words = execute_query_safe(GET_SENTENCE, {'speech_id': speech_id, 'paragraph': paragraph,
                                                           'sentence': sentence}, True)
        full_sentence = ""

        # Build the sentence
        for curr_word in sentence_words:
            full_sentence = "{} {}".format(full_sentence, curr_word[0].strip())

        return {'speech_id': speech_id, 'paragraph': paragraph, 'sentence': sentence, 'index': index,
                'word': word[1].strip(), 'full_sentence': full_sentence}


def get_all_words_in_speech(speech_id):
    if speech_id is None:
        abort(400, 'No Speech Id given')

    results = []
    words = execute_query_safe(GET_SPEECH_WORDS, {'speech_id': speech_id}, True)

    for word in words:
        results.append({'id': word[0], 'word': word[1].strip()})

    return results
