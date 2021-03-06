import re
from flask_restful import Resource
from flask import request, jsonify, abort
from flask_jwt import jwt_required

from src.DBUtils import execute_query_safe, execute_insert_many_safe
from src.queries import NEW_SPEECH, NEW_WORD, ADD_WORD_TO_SPEECH, GET_ALL_SPEECHES, \
    GET_WORD, SEARCH_SPEECH, GET_SPEECH, ADD_WORD_TO_SPEECH_VAL, GET_SENTENCE, GET_SPEECH_DETAILS, GET_ALL_WORDS


class Speech(Resource):
    @jwt_required()
    def get(self):
        if 'id' in request.args:
            return jsonify(get_speech(request.args['id']))

        elif 'query' in request.args:
            return search_speech(request.args['query'])

        return get_all_speeches()

    @jwt_required()
    def post(self):
        data = request.get_json()
        create_new_speech(data.get('name'), data.get('speaker'), data.get('date'), data.get('location'),
                          data.get('file_path'))


def create_new_speech(name, speaker, date, location, file_path):
    if name is None or file_path is None:
        abort(400, 'Must get all of the required fields of the speech')

    # Insert to Speech table
    speech = execute_query_safe(NEW_SPEECH, {'speech_name': name, 'speaker': speaker, 'date': date,
                                             'location': location, 'file_path': file_path}, True, True)

    if speech is None:
        abort(500, 'Cannot crate speech')

    speech_id = speech[0]

    # Get the tst from the file
    file = open(file_path, 'r', encoding="utf8")
    try:
        paragraphs = file.readlines()
    finally:
        file.close()

    paragraph_index = 1

    # Build a words' dictionary
    all_words = execute_query_safe(GET_ALL_WORDS, is_fetch=True)
    word_dict = {}
    for word in all_words:
        word_dict[word[1].strip()] = word[0]

    # Go over each paragraph
    for curr_paragraph in paragraphs:

        if curr_paragraph != '\n':
            # Split to sentences
            sentences = re.split('([\\S]+?[[\\S\\s]+?(?:[.?!]))', curr_paragraph)
            sentence_index = 1
            words_to_insert = []

            # Go over each sentence
            for curr_sentence in sentences:

                if curr_sentence != "" and curr_sentence != " ":
                    # Split to words
                    words = curr_sentence.split()
                    word_index = 1

                    # Go over the words
                    for curr_word in words:

                        if curr_word != "":
                            actual_word = curr_word
                            only_word = re.sub(r'[^\w\s]', '', curr_word).lower()

                            # Try to find the word in the dictionary
                            word_id = word_dict.get(only_word)

                            # If not found - adds it
                            if word_id is None:
                                word = execute_query_safe(NEW_WORD, {'word': only_word, 'length': len(only_word)},
                                                          True, True)
                                word_id = word[0]
                                word_dict[only_word] = word_id

                            words_to_insert.append((word_id, speech_id, paragraph_index, sentence_index, word_index,
                                                    actual_word))
                            word_index += 1
                    sentence_index += 1
            # Add the whole paragraph to the DB
            execute_insert_many_safe(ADD_WORD_TO_SPEECH, words_to_insert, ADD_WORD_TO_SPEECH_VAL)
            paragraph_index += 1


def get_speech(speech_id):
    if speech_id is None:
        abort(400, 'No Speech Id given')

    speech_details = execute_query_safe(GET_SPEECH_DETAILS, {'speech_id': speech_id}, True, True)

    if speech_details is None:
        abort(500, 'No Speech with id {}'.format(speech_id))

    words = execute_query_safe(GET_SPEECH, {'speech_id': speech_id}, True)
    full_speech = ""
    curr_paragraph = 1

    # Builds the speech back
    for curr_word in words:
        # If its an end of the paragraph
        if curr_word[0] == curr_paragraph:
            full_speech = "{} {}".format(full_speech, curr_word[3].strip())
        else:
            full_speech = "{}\n\n{}".format(full_speech, curr_word[3].strip())
            curr_paragraph = curr_word[0]

    return {'speech_id': speech_id,
            'name': speech_details[0].strip(),
            'speaker': speech_details[1].strip(),
            'location': speech_details[2].strip(),
            'date': speech_details[3],
            'full_text': full_speech}


def search_speech(query):
    if query is None:
        abort(400, 'No query to search')

    results = {}
    results_list = []
    sql_query = '%' + query + '%'
    sentences = execute_query_safe(SEARCH_SPEECH, {'word': sql_query, 'speech_name': sql_query, 'speaker': sql_query,
                                                   'location': sql_query}, True)

    if sentences is None or len(sentences) == 0:
        abort(500, 'No speeches found with query - {}'.format(query))

    for sentence in sentences:
        speech_id = sentence[3]

        # Add the speech to the results
        if speech_id not in results:
            results[speech_id] = {'id': speech_id, 'name': sentence[0].strip(), 'speaker': sentence[1].strip(),
                                  'location': sentence[2].strip(), 'text': ''}
        # If there is a sentence, add to text
        if sentence[4] != 0:
            words_in_sentence = execute_query_safe(GET_SENTENCE, {'speech_id': speech_id, 'paragraph': sentence[4],
                                                                  'sentence': sentence[5]}, True)
            full_sentence = ""

            # Build the sentence
            for curr_word in words_in_sentence:
                full_sentence = "{} {}".format(full_sentence, curr_word[0].strip())

            # Make the search word as bold
            # full_sentence = full_sentence.replace(query, "<b>" + query + "</b>")

            # Add Sentence to results
            results[speech_id]['text'] = "{}...{}".format(results[speech_id]['text'], full_sentence)

    # Convert the dictionary to list
    for value in results.values():
        results_list.append(value)

    return results_list


def get_all_speeches():
    results = []
    speeches = execute_query_safe(GET_ALL_SPEECHES, is_fetch=True)

    for speech in speeches:
        results.append({'id': speech[0], 'name': speech[1].strip()})

    return results
