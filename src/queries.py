# Speeches
NEW_SPEECH = '''INSERT INTO public."Speech"(
speech_id, speech_name, speaker, date, location, file_path)
VALUES ((SELECT max(speech_id)+1 from public."Speech"), '{}', '{}', '{}', '{}', '{}')
returning speech_id;'''

ADD_WORD_TO_SPEECH = '''INSERT INTO public."Word_in_Speech"(
word_id, speech_id, paragraph, sentence, index_in_sentence, actual_word)
VALUES {} '''

ADD_WORD_TO_SPEECH_VAL = ''' ('{}', '{}', '{}', '{}', '{}', '{}'),'''

GET_SPEECH = '''SELECT paragraph, sentence, index_in_sentence, actual_word FROM public."Word_in_Speech"
WHERE speech_id = '{}' ORDER BY paragraph, sentence, index_in_sentence;'''

# TODO: write this super important query
SEARCH_SPEECH = '''SELECT distinct b.speech_id, paragraph, sentence, index_in_sentence
FROM public."Speech" as a
join public."Word_in_Speech" as b on a.speech_id = b.speech_id
join public."Word" as c on b.word_id = c.word_id
where speech_name like '%{query}%' or speaker like '%{query}%' or word like '%{query}%' '''

# Words
NEW_WORD = '''INSERT INTO public."Word"(
word_id, word, length)
VALUES ((SELECT max(word_id)+1 from public."Word"), '{}', '{}')
on conflict (word) do nothing
returning word_id;'''

GET_WORD = '''SELECT word_id FROM public."Word" WHERE word = ('{}')'''

LAST_WORD_INDEX = '''SELECT MAX(word_id) FROM public."Word"'''

# Phrases
NEW_PHRASE_PART = '''INSERT INTO public."Word_Phrase"(
index, phrase_id, word_id)
VALUES ('{}', '{}', '{}');'''

LAST_PHRASE_INDEX = '''SELECT MAX(phrase_id) FROM public."Phrase"'''

# TODO: enable search by multiple words
SEARCH_PHRASE = '''SELECT index, word
FROM public."Word_Phrase" as a
join public."Word" as b on a.word_id = b.word_id
where phrase_id = (SELECT phrase_id
FROM public."Word_Phrase" as a
join public."Word" as b on a.word_id = b.word_id
where word like '%'{}'%')
order by index;'''

# Groups
NEW_GROUP = '''INSERT INTO public."Group"(
group_id, group_name)
VALUES ((SELECT max(group_id)+1 FROM public."Group"), '{}')
on conflict (group_name) do nothing
returning group_id'''

ADD_WORD_TO_GROUP = '''INSERT INTO public."Word_in_Group"(
word_id, group_id)
VALUES ('{}', '{}');'''

SEARCH_GROUP = '''SELECT group_id, group_name
FROM public."Group"
where group_name like '%'{}'%';'''

GET_GROUP = '''SELECT b.word_id, word
FROM public."Word_in_Group" as a
join public."Word" as b on a.word_id = b.word_id
where group_id = '{}';'''
