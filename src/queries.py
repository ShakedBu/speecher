# Speeches
NEW_SPEECH = '''INSERT INTO public."Speech"(
speech_id, speech_name, speaker, date, location, file_path)
VALUES ((SELECT max(speech_id)+1 from public."Speech"), '{}', '{}', '{}', '{}', '{}')
returning speech_id;'''

ADD_WORD_TO_SPEECH = '''INSERT INTO public."Word_in_Speech"(
word_id, speech_id, paragraph, sentence, index_in_sentence, actual_word)
VALUES {} '''

ADD_WORD_TO_SPEECH_VAL = ''' ('{}', '{}', '{}', '{}', '{}', '{}'),'''

# Bad Example
GET_SPEECH = '''SELECT paragraph, sentence, index_in_sentence, actual_word FROM public."Word_in_Speech"
WHERE speech_id = '{}' ORDER BY paragraph, sentence, index_in_sentence;'''
# Good example
# GET_SPEECH = '''SELECT paragraph, sentence, index_in_sentence, actual_word FROM public."Word_in_Speech"
# WHERE speech_id = %s ORDER BY paragraph, sentence, index_in_sentence;'''

GET_SPEECH_DETAILS = '''SELECT speech_name, speaker, location, date
FROM public."Speech"
WHERE speech_id = '{}' '''

SEARCH_SPEECH = '''SELECT speech_name, speaker, location, b.speech_id, paragraph, sentence
FROM public."Speech" as a
join public."Word_in_Speech" as b on a.speech_id = b.speech_id
join public."Word" as c on b.word_id = c.word_id
where word like lower('%{}%')
union select speech_name, speaker, location, speech_id, 0, 0
FROM public."Speech"
where lower(speech_name) like lower('%{}%') or 
lower(speaker) like lower('%{}%') or 
lower(location) like lower('%{}%')
order by speech_id, paragraph, sentence;'''

GET_SENTENCE = '''select actual_word
from public."Word_in_Speech"
where speech_id = '{}' and paragraph = '{}' and sentence = '{}'
order by speech_id, paragraph, sentence;'''

GET_SPEECH_WORDS = '''SELECT distinct a.word_id, word
FROM public."Word_in_Speech" as a
JOIN public."Word" as b on a.word_id = b.word_id
WHERE speech_id = '{}'
order by word;'''

# Words
NEW_WORD = '''INSERT INTO public."Word"(
word_id, word, length)
VALUES ((SELECT max(word_id)+1 from public."Word"), '{}', '{}')
on conflict (word) do nothing
returning word_id;'''

GET_WORD = '''SELECT word_id FROM public."Word" WHERE word = ('{}')'''

LAST_WORD_INDEX = '''SELECT MAX(word_id) FROM public."Word"'''

GET_WORD_BY_LOC = '''SELECT a.word_id, word
FROM public."Word_in_Speech" as a
JOIN public."Word" as b on a.word_id = b.word_id
WHERE speech_id = '{}' and paragraph = '{}' and sentence = '{}' and index_in_sentence = '{}';'''

GET_ALL_WORDS = '''SELECT word_id, word
FROM public."Word"
ORDER BY word;'''

GET_WORD_APPEARANCES_IN_SPEECH = '''SELECT paragraph, sentence, index_in_sentence
FROM public."Word_in_Speech"
where speech_id = '{}' and lower(actual_word) like lower('%{}%')
order by paragraph, sentence, index_in_sentence;'''

GET_PARTIAL_SENTENCE = '''SELECT actual_word
from public."Word_in_Speech"
where speech_id = '{}' and paragraph = '{}' and sentence = '{}' and index_in_sentence - '{}' 
BETWEEN -{range} and {range}
order by paragraph, sentence, index_in_sentence;'''

# Phrases
NEW_PHRASE_PART = '''INSERT INTO public."Word_Phrase"(
index, phrase_id, word_id)
VALUES ('{}', '{}', '{}');'''

LAST_PHRASE_INDEX = '''SELECT MAX(phrase_id)+1 FROM public."Word_Phrase"'''

SEARCH_PHRASE_FIRST = '''select paragraph, sentence, index_in_sentence
from public."Word_in_Speech" as a{index}
where speech_id = '{}' and a{index}.word_id = '{}' and exists ({})
order by paragraph, sentence, index_in_sentence;'''

SEARCH_PHRASE_MIDDLE = '''select paragraph, sentence, index_in_sentence
from public."Word_in_Speech" as a{index}
where speech_id = '{}' and a{index}.word_id = '{}' and 
a{previous_index}.paragraph = a{index}.paragraph and a{previous_index}.sentence = a{index}.sentence and 
a{previous_index}.index_in_sentence = a{index}.index_in_sentence-1 and exists ({})'''

SEARCH_PHRASE_LAST = '''select paragraph, sentence, index_in_sentence
from public."Word_in_Speech" as a{index}
where speech_id = '{}' and a{index}.word_id = '{}' and 
a{previous_index}.paragraph = a{index}.paragraph and a{previous_index}.sentence = a{index}.sentence and 
a{previous_index}.index_in_sentence = a{index}.index_in_sentence-1'''

GET_ALL_PHRASES = '''SELECT phrase_id, index, a.word_id, word
FROM public."Word_Phrase" as a
inner join public."Word" as b on a.word_id = b.word_id
order by phrase_id, index;'''

GET_PHRASE = '''select index, word_id
from public."Word_Phrase"
where phrase_id = '{}'
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

DELETE_WORD_FROM_GROUP = '''DELETE FROM public."Word_in_Group"
WHERE group_id = '{}' AND word_id = '{}';'''

SEARCH_GROUP = '''SELECT group_id, group_name
FROM public."Group"
where group_name like '%'{}'%';'''

GET_GROUP = '''SELECT b.word_id, word
FROM public."Word_in_Group" as a
join public."Word" as b on a.word_id = b.word_id
where group_id = '{}';'''

GET_ALL_GROUPS = '''SELECT group_id, group_name
FROM public."Group";'''

# Statistics
GET_ALL_COUNTS = '''select paragraph, sentence, count(word_id)
from public."Word_in_Speech"
where speech_id='{}'
group by paragraph, sentence
order by paragraph, sentence;'''

COUNT_CHARS_IN_WORD = '''select sum(length)
from public."Word_in_Speech" as a
inner join public."Word" as b on a.word_id = b.word_id
Where speech_id = '{}' and paragraph = '{}' and sentence = '{}' and index_in_sentence = '{}';'''

COUNT_CHARS_IN_SENTENCE = '''select sum(length)
from public."Word_in_Speech" as a
inner join public."Word" as b on a.word_id = b.word_id
Where speech_id = '{}' and paragraph = '{}' and sentence = '{}';'''

COUNT_CHARS_IN_PARAGRAPH = '''select sum(length)
from public."Word_in_Speech" as a
inner join public."Word" as b on a.word_id = b.word_id
Where speech_id = '{}' and paragraph = '{}';'''

COUNT_CHARS_IN_SPEECH = '''select sum(length)
from public."Word_in_Speech" as a
inner join public."Word" as b on a.word_id = b.word_id
Where speech_id = '{}';'''

COUNT_WORDS_IN_SENTENCE = '''select count(*)
from public."Word_in_Speech"
Where speech_id = '{}' and paragraph = '{}' and sentence = '{}';'''

COUNT_WORDS_IN_PARAGRAPH = '''select count(*)
from public."Word_in_Speech"
Where speech_id = '{}' and paragraph = '{}';'''

COUNT_WORDS_IN_SPEECH = '''select count(*)
from public."Word_in_Speech"
Where speech_id = '{}';'''