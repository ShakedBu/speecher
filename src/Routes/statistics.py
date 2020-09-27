from flask_restful import Resource
from flask import request

from src.DBUtils import execute_query
from src.queries import GET_ALL_COUNTS, COUNT_CHARS_IN_WORD, COUNT_CHARS_IN_SENTENCE, COUNT_CHARS_IN_PARAGRAPH, \
    COUNT_CHARS_IN_SPEECH, COUNT_WORDS_IN_SENTENCE, COUNT_WORDS_IN_PARAGRAPH, COUNT_WORDS_IN_SPEECH


class Statistics(Resource):
    def get(self):
        if 'speech_id' in request.args:
            if 'count' in request.args:
                if request.args['count'] == 'char':
                    return count_chars(request.args['speech_id'], request.args.get('paragraph'),
                                       request.args.get('sentence'), request.args.get('word'))
                return count_words(request.args['speech_id'], request.args.get('paragraph'),
                                   request.args.get('sentence'))
        return get_general_counts_by_speech(request.args['speech_id'])


def get_general_counts_by_speech(speech_id):
    results = []
    counts = execute_query(GET_ALL_COUNTS.format(speech_id), True)
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
            words = execute_query(COUNT_WORDS_IN_SENTENCE.format(speech_id, paragraph, sentence), True, True)
        else:
            words = execute_query(COUNT_WORDS_IN_PARAGRAPH.format(speech_id, paragraph), True, True)
    else:
        words = execute_query(COUNT_WORDS_IN_SPEECH.format(speech_id), True, True)

    return words[0]


def count_chars(speech_id, paragraph, sentence, word):
    if paragraph is not None:
        if sentence is not None:
            if word is not None:
                chars = execute_query(COUNT_CHARS_IN_WORD.format(speech_id, paragraph, sentence, word), True, True)
            else:
                chars = execute_query(COUNT_CHARS_IN_SENTENCE.format(speech_id, paragraph, sentence), True)
        else:
            chars = execute_query(COUNT_CHARS_IN_PARAGRAPH.format(speech_id, paragraph), True)
    else:
        chars = execute_query(COUNT_CHARS_IN_SPEECH.format(speech_id), True)

    return chars[0]


def count_words_appearances(speech_id):
    return 0
