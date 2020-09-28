from flask_restful import Resource
from flask import request

from src.DBUtils import execute_query_safe
from src.queries import GET_ALL_COUNTS, COUNT_CHARS_IN_WORD, COUNT_CHARS_IN_SENTENCE, COUNT_CHARS_IN_PARAGRAPH, \
    COUNT_CHARS_IN_SPEECH, COUNT_WORDS_IN_SENTENCE, COUNT_WORDS_IN_PARAGRAPH, COUNT_WORDS_IN_SPEECH, \
    WORD_APPEARANCES, WORD_APPEARANCES_IN_SPEECH


class Statistics(Resource):
    def get(self):
        if 'count' in request.args:
            if request.args['count'] == 'chars':
                return count_chars(request.args.get('speech_id'), request.args.get('paragraph'),
                                   request.args.get('sentence'), request.args.get('word'))
            if request.args['count'] == 'words':
                return count_words(request.args.get('speech_id'), request.args.get('paragraph'),
                                   request.args.get('sentence'))
            if request.args['count'] == 'appearances':
                return count_words_appearances(request.args.get('speech_id'))

        return get_general_counts_by_speech(request.args['speech_id'])


def get_general_counts_by_speech(speech_id):
    if speech_id is None:
        return 'No Speech Id given', 400

    results = []
    counts = execute_query_safe(GET_ALL_COUNTS, {'speech_id': speech_id}, True)
    paragraph_index = 1
    paragraph_sentences = []

    for count in counts:
        if count[0] == paragraph_index:
            paragraph_sentences.append({'sentence': count[1], 'words': count[2]})
        else:
            results.append({'paragraph': paragraph_index, 'sentences': paragraph_sentences})
            paragraph_index += 1
            paragraph_sentences = [{'sentence': count[1], 'words': count[2]}]

    results.append({'paragraph': paragraph_index, 'sentences': paragraph_sentences})

    return results


def count_words(speech_id, paragraph, sentence):
    if paragraph is not None:
        if sentence is not None:
            words = execute_query_safe(COUNT_WORDS_IN_SENTENCE, {'speech_id': speech_id, 'paragraph': paragraph,
                                                                 'sentence': sentence}, True, True)
        else:
            words = execute_query_safe(COUNT_WORDS_IN_PARAGRAPH, {'speech_id': speech_id, 'paragraph': paragraph},
                                       True, True)
    else:
        words = execute_query_safe(COUNT_WORDS_IN_SPEECH, {'speech_id': speech_id}, True, True)

    return words[0]


def count_chars(speech_id, paragraph, sentence, word):
    if speech_id is None:
        return 'Speech Id is Obligated field', 400

    if paragraph is not None:
        if sentence is not None:
            if word is not None:
                chars = execute_query_safe(COUNT_CHARS_IN_WORD, {'speech_id': speech_id, 'paragraph': paragraph,
                                                                 'sentence': sentence, 'word': word}, True, True)
            else:
                chars = execute_query_safe(COUNT_CHARS_IN_SENTENCE, {'speech_id': speech_id, 'paragraph': paragraph,
                                                                     'sentence': sentence}, True, True)
        else:
            chars = execute_query_safe(COUNT_CHARS_IN_PARAGRAPH, {'speech_id': speech_id, 'paragraph': paragraph}, True,
                                       True)
    else:
        chars = execute_query_safe(COUNT_CHARS_IN_SPEECH, {'speech_id': speech_id}, True, True)

    return chars[0]


def count_words_appearances(speech_id):
    results = []

    if speech_id is not None:
        appearances = execute_query_safe(WORD_APPEARANCES_IN_SPEECH, {'speech_id': speech_id}, True)
    else:
        appearances = execute_query_safe(WORD_APPEARANCES, is_fetch=True)

    for word in appearances:
        results.append({'id': word[0], 'word': word[1].strip(), 'appearances': word[2]})

    return results
