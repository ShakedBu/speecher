import re

from src.DBUtils import execute_query
from src.queries import NEW_SPEECH, FIND_WORD, LAST_WORD_INDEX, NEW_WORD, ADD_WORD_TO_SPEECH


def create_new_speech(name, speaker, date, location, file_path, text):
    # Insert to Speech table
    speech = execute_query(NEW_SPEECH, (name, speaker, date, location, file_path), True)

    # Go over the speech actual text
    paragraphes = text.split('\n\n')
    paragraph_index = 1

    for curr_paragraph in paragraphes:
        sentences = re.split('[.?!]', curr_paragraph)
        sentence_index = 1

        for curr_sentence in sentences:
            words = curr_sentence.split()
            word_index = 1

            for curr_word in words:
                # Get suffix and prefix
                suffix = ""
                prefix = ""

                # Check if the word exists in DB already
                word_id = execute_query((FIND_WORD, curr_word), True)[0][0]

                if word_id == '':
                    # Add the new word to DB
                    word_id = execute_query(LAST_WORD_INDEX, True)[0]
                    word_id += 1
                    execute_query((NEW_WORD, (word_id, curr_word), True))

                # Add the word into the speech in DB
                execute_query((ADD_WORD_TO_SPEECH, (word_id, speech[0], paragraph_index,
                                                    sentence_index, word_index, prefix, suffix)),
                              True)

                word_index += 1

            sentence_index += 1

        paragraph_index += 1
