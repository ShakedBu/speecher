import re

from src.DBUtils import execute_query
from src.queries import NEW_SPEECH, NEW_WORD, ADD_WORD_TO_SPEECH, GET_WORD


def create_new_speech(name, speaker, date, location, file_path, text):
    # Insert to Speech table
    speech = execute_query(NEW_SPEECH, (name, speaker, date, location, file_path), True)

    # Go over the speech actual text and index it
    paragraphs = text.split('\n\n')
    paragraph_index = 1

    # Go over each paragraph
    for curr_paragraph in paragraphs:
        # Split to sentences
        sentences = re.split('[.?!]', curr_paragraph)
        sentence_index = 1

        # Go over each sentence
        for curr_sentence in sentences:
            # Split to words
            words = curr_sentence.split()
            word_index = 1

            # Go over the words
            for curr_word in words:
                # Get suffix and prefix and actual word
                prefix, actual_word, suffix = re.split(curr_word, '(\\W)(\\w*)(\\W*)')

                # Try to find the word in the DB
                word = execute_query((GET_WORD, actual_word), True)

                # If found - gets id otherwise adds it
                if word[0] != 0:
                    word_id = word[0]
                else:
                    word = execute_query((NEW_WORD, (word_id, actual_word), True))
                    word_id = word[0]

                # Add the word into the speech in DB
                execute_query((ADD_WORD_TO_SPEECH, (word_id, speech[0], paragraph_index,
                                                    sentence_index, word_index, prefix, suffix)),
                              True)

                word_index += 1
            sentence_index += 1
        paragraph_index += 1


def search_speech(query):
    return ''
