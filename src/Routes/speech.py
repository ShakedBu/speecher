import re
from flask_restful import Resource
from flask import request, jsonify

from src.DBUtils import execute_query
from src.queries import NEW_SPEECH, NEW_WORD, ADD_WORD_TO_SPEECH, \
    GET_WORD, SEARCH_SPEECH, GET_SPEECH, ADD_WORD_TO_SPEECH_VAL, GET_SENTENCE, GET_SPEECH_DETAILS


class Speech(Resource):
    def get(self):
        if 'id' in request.args:
            return jsonify(get_speech(request.args['id']))

        elif 'query' in request.args:
            return search_speech(request.args['query'])

    def post(self):
        data = request.get_json()
        create_new_speech(data['name'], data['speaker'], data['date'], data['location'], data['file_path'])


def create_new_speech(name, speaker, date, location, file_path):
    # Insert to Speech table
    speech = execute_query(NEW_SPEECH.format(name, speaker, date, location, file_path), True, True)
    speech_id = speech[0]

    # Get the tst from the file
    file = open(file_path, 'r', encoding="utf8")
    try:
        paragraphs = file.readlines()
    finally:
        file.close()

    # paragraphs = text.split('\n\n')
    paragraph_index = 1

    # Go over each paragraph
    for curr_paragraph in paragraphs:

        if curr_paragraph != '\n':
            # Split to sentences
            sentences = re.split('([\\S]+?[[\\S\\s]+?(?:[.?!]))', curr_paragraph)
            sentence_index = 1
            # Go over each sentence
            for curr_sentence in sentences:

                if curr_sentence != "" and curr_sentence != " ":
                    # Split to words
                    words = curr_sentence.split()
                    word_index = 1
                    sentence_insert = ""

                    # Go over the words
                    for curr_word in words:

                        if curr_word != "":
                            actual_word = curr_word
                            only_word = re.findall('(\\w*)', curr_word)[0].lower()

                            # Try to find the word in the DB
                            word = execute_query(GET_WORD.format(only_word), True, True)

                            # If found - gets id otherwise adds it
                            if word is not None:
                                word_id = word[0]
                            else:
                                word = execute_query(NEW_WORD.format(only_word, len(only_word)), True, True)
                                word_id = word[0]

                            sentence_insert += ADD_WORD_TO_SPEECH_VAL.format(word_id, speech_id,
                                                                             paragraph_index, sentence_index,
                                                                             word_index, actual_word)
                            word_index += 1

                    # Add the whole sentence to the DB
                    execute_query(ADD_WORD_TO_SPEECH.format(sentence_insert.rstrip(',')))
                    sentence_index += 1
            paragraph_index += 1


def get_speech(speech_id):
    speech_details = execute_query(GET_SPEECH_DETAILS.format(speech_id), True, True)
    words = execute_query(GET_SPEECH.format(speech_id), True)
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
    results = {}
    results_list = []
    sentences = execute_query(SEARCH_SPEECH.format(query, query, query, query), True)

    for sentence in sentences:
        speech_id = sentence[3]

        # Add the speech to the results
        if speech_id not in results:
            results[speech_id] = {'id': speech_id, 'name': sentence[0].strip(), 'speaker': sentence[1].strip(),
                                  'location': sentence[2].strip(), 'text': ''}
        # If there is a sentence, add to text
        if sentence[4] != 0:
            words_in_sentence = execute_query(GET_SENTENCE.format(speech_id, sentence[4], sentence[5]), True)
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