NEW_SPEECH = '''INSERT INTO public."Speech"(
speech_id, speech_name, speaker, date, location, file_path)
VALUES (?, ?, ?, ?, ?, ?);
'''

NEW_WORD = '''INSERT INTO public."Word"(
word_id, word) 
VALUES (?, ?)
ON CONFLICT (word) DO NOTHING;'''

NEW_PHRASE_PART = '''INSERT INTO public."Word_Phrase"(
index, phrase_id, word_id)
VALUES (?, ?, ?);'''

NEW_GROUP = '''INSERT INTO public."Group"(
group_id, group_name)
VALUES (?, ?);'''

FIND_WORD = '''SELECT word_id FROM public."Word" WHERE word = (?)'''

LAST_WORD_INDEX = '''SELECT MAX(word_id) FROM public."Word"'''

ADD_WORD_TO_SPEECH = '''INSERT INTO public."Word_in_Speech"(
word_id, speech_id, paragraph, sentence, index_in_sentence, prefix, suffix)
VALUES (?, ?, ?, ?, ?, ?, ?);'''

LAST_PHRASE_INDEX = '''SELECT MAX(phrase_id) FROM public."Phrase"'''

LAST_GROUP_INDEX = '''SELECT MAX(group_id) FROM public."Group"'''

ADD_WORD_TO_GROUP = '''INSERT INTO public."Word_in_Group"(
word_id, group_id)
VALUES (?, ?);'''