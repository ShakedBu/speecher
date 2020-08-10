import re

from src.DBUtils import execute_query
from src.queries import NEW_SPEECH, NEW_WORD, ADD_WORD_TO_SPEECH, \
    GET_WORD, SEARCH_SPEECH, GET_SPEECH, ADD_WORD_TO_SPEECH_VAL


def create_new_speech(name, speaker, date, location, file_path):
    # Insert to Speech table
    # TODO: remember to set date format
    # TODO: set speech_name as unique
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
            sentences = re.split('([\\S]+?[[\\S\\s]+?(?:[\\.?!]))', curr_paragraph)
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
                            # Get suffix and prefix and actual word
                            actual_word = re.findall('(\\w*)', curr_word)[0]
                            word_parts = re.split('(\\W*)(\\W*)(\\w*)', curr_word)
                            word_parts = list(filter(None, word_parts))
                            prefix = '' if word_parts[0] == actual_word else word_parts[0]
                            suffix = word_parts[-1] if word_parts[-1] != actual_word else ''

                            # Try to find the word in the DB
                            word = execute_query(GET_WORD.format(actual_word), True, True)

                            # If found - gets id otherwise adds it
                            if word is not None:
                                word_id = word[0]
                            else:
                                word = execute_query(NEW_WORD.format(actual_word, len(actual_word)), True, True)
                                word_id = word[0]

                            sentence_insert += ADD_WORD_TO_SPEECH_VAL.format(word_id, speech_id,
                                                                             paragraph_index, sentence_index,
                                                                             word_index, prefix, suffix)
                            word_index += 1

                    # Add the whole sentence to the DB
                    execute_query(ADD_WORD_TO_SPEECH.format(sentence_insert.rstrip(',')))
                    sentence_index += 1
            paragraph_index += 1


def get_speech(speech_id):
    words = execute_query(GET_SPEECH.format(speech_id), True)
    full_speech = ""
    curr_paragraph = 1

    # Builds the speech back
    for curr_word in words:
        # If its an end of the paragraph
        if curr_word[1] == curr_paragraph:
            full_speech = "{} {}".format(full_speech,
                                         curr_word[4].strip() + curr_word[0].strip() + curr_word[5].strip())
        else:
            full_speech = "{}\n\n{}".format(full_speech,
                                            curr_word[4].strip() + curr_word[0].strip() + curr_word[5].strip())
            curr_paragraph = curr_word[1]

    return full_speech


def search_speech(query):
    return execute_query((SEARCH_SPEECH, query))
