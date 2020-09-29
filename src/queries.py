# Speeches
NEW_SPEECH = '''INSERT INTO public."Speech"(
speech_id, speech_name, speaker, date, location, file_path)
VALUES ((SELECT max(speech_id)+1 from public."Speech"), %(speech_name)s, %(speaker)s, %(date)s, %(location)s, 
%(file_path)s)
returning speech_id;'''

ADD_WORD_TO_SPEECH = '''INSERT INTO public."Word_in_Speech"(
word_id, speech_id, paragraph, sentence, index_in_sentence, actual_word)
VALUES %s'''

ADD_WORD_TO_SPEECH_VAL = '''(%s, %s, %s, %s, %s, %s)'''

# Bad Example
# GET_SPEECH = '''SELECT paragraph, sentence, index_in_sentence, actual_word FROM public."Word_in_Speech"
# WHERE speech_id = '{}' ORDER BY paragraph, sentence, index_in_sentence;'''
# Good example
GET_SPEECH = '''SELECT paragraph, sentence, index_in_sentence, actual_word FROM public."Word_in_Speech"
WHERE speech_id = %(speech_id)s ORDER BY paragraph, sentence, index_in_sentence;'''

GET_SPEECH_DETAILS = '''SELECT speech_name, speaker, location, date
FROM public."Speech"
WHERE speech_id = %(speech_id)s '''

SEARCH_SPEECH = '''SELECT speech_name, speaker, location, b.speech_id, paragraph, sentence
FROM public."Speech" as a
join public."Word_in_Speech" as b on a.speech_id = b.speech_id
join public."Word" as c on b.word_id = c.word_id
where word like lower(%(word)s)
union select speech_name, speaker, location, speech_id, 0, 0
FROM public."Speech"
where lower(speech_name) like lower(%(speech_name)s) or 
lower(speaker) like lower(%(speaker)s) or 
lower(location) like lower(%(location)s)
order by speech_id, paragraph, sentence;'''

GET_SENTENCE = '''select actual_word
from public."Word_in_Speech"
where speech_id = %(speech_id)s and paragraph = %(paragraph)s and sentence = %(sentence)s
order by speech_id, paragraph, sentence;'''

GET_SPEECH_WORDS = '''SELECT distinct a.word_id, word
FROM public."Word_in_Speech" as a
JOIN public."Word" as b on a.word_id = b.word_id
WHERE speech_id = %(speech_id)s
order by word;'''

GET_ALL_SPEECHES = '''select speech_id, speech_name
from public."Speech"'''

# Words
NEW_WORD = '''INSERT INTO public."Word"(
word_id, word, length)
VALUES ((SELECT max(word_id)+1 from public."Word"), %(word)s, %(length)s)
on conflict (word) do nothing
returning word_id;'''

GET_WORD = '''SELECT word_id FROM public."Word" WHERE word = %(word)s'''

LAST_WORD_INDEX = '''SELECT MAX(word_id) FROM public."Word"'''

GET_WORD_BY_LOC = '''SELECT a.word_id, word
FROM public."Word_in_Speech" as a
JOIN public."Word" as b on a.word_id = b.word_id
WHERE speech_id = %(speech_id)s and paragraph = %(paragraph)s and sentence = %(sentence)s and 
index_in_sentence = %(index)s;'''

GET_ALL_WORDS = '''SELECT word_id, word
FROM public."Word"
ORDER BY word;'''

GET_WORD_APPEARANCES_IN_SPEECH = '''SELECT paragraph, sentence, index_in_sentence
FROM public."Word_in_Speech"
where speech_id = %(speech_id)s and lower(actual_word) like lower(%(word)s)
order by paragraph, sentence, index_in_sentence;'''

GET_PARTIAL_SENTENCE = '''SELECT actual_word
from public."Word_in_Speech"
where speech_id = %(speech_id)s and paragraph = %(paragraph)s and sentence = %(sentence)s and 
index_in_sentence - %(index)s BETWEEN -%(range)s and %(range)s
order by paragraph, sentence, index_in_sentence;'''

# Phrases
NEW_PHRASE_PART = '''INSERT INTO public."Word_Phrase"(
index, phrase_id, word_id)
VALUES (%(index)s, %(phrase_id)s, %(word_id)s);'''

LAST_PHRASE_INDEX = '''SELECT MAX(phrase_id)+1 FROM public."Word_Phrase"'''

SEARCH_PHRASE_FIRST = '''select paragraph, sentence, index_in_sentence
from public."Word_in_Speech" as a{index}
where speech_id = %s and a{index}.word_id = %s and exists ({})
order by paragraph, sentence, index_in_sentence;'''

SEARCH_PHRASE_MIDDLE = '''select paragraph, sentence, index_in_sentence
from public."Word_in_Speech" as a{index}
where speech_id = %s and a{index}.word_id = %s and 
a{previous_index}.paragraph = a{index}.paragraph and a{previous_index}.sentence = a{index}.sentence and 
a{previous_index}.index_in_sentence = a{index}.index_in_sentence-1 and exists ({})'''

SEARCH_PHRASE_LAST = '''select paragraph, sentence, index_in_sentence
from public."Word_in_Speech" as a{index}
where speech_id = %s and a{index}.word_id = %s and 
a{previous_index}.paragraph = a{index}.paragraph and a{previous_index}.sentence = a{index}.sentence and 
a{previous_index}.index_in_sentence = a{index}.index_in_sentence-1'''

GET_ALL_PHRASES = '''SELECT phrase_id, index, a.word_id, word
FROM public."Word_Phrase" as a
inner join public."Word" as b on a.word_id = b.word_id
order by phrase_id, index;'''

GET_PHRASE = '''select index, word_id
from public."Word_Phrase"
where phrase_id = %(phrase_id)s
order by index;'''

# Groups
NEW_GROUP = '''INSERT INTO public."Group"(
group_id, group_name)
VALUES ((SELECT max(group_id)+1 FROM public."Group"), %(group_name)s)
on conflict (group_name) do nothing
returning group_id'''

ADD_WORD_TO_GROUP = '''INSERT INTO public."Word_in_Group"(
word_id, group_id)
VALUES (%(word_id)s, %(group_id)s);'''

DELETE_WORD_FROM_GROUP = '''DELETE FROM public."Word_in_Group"
WHERE group_id = %(group_id)s AND word_id = %(word_id)s;'''

SEARCH_GROUP = '''SELECT group_id, group_name
FROM public."Group"
where group_name like %(query)s;'''

GET_GROUP = '''SELECT b.word_id, word
FROM public."Word_in_Group" as a
join public."Word" as b on a.word_id = b.word_id
where group_id = %(group_id)s;'''

GET_ALL_GROUPS = '''SELECT group_id, group_name
FROM public."Group";'''

# Statistics
GET_ALL_COUNTS = '''select paragraph, sentence, count(word_id)
from public."Word_in_Speech"
where speech_id= %(speech_id)s
group by paragraph, sentence
order by paragraph, sentence;'''

COUNT_CHARS_IN_WORD = '''select sum(length)
from public."Word_in_Speech" as a
inner join public."Word" as b on a.word_id = b.word_id
Where speech_id = %(speech_id)s and paragraph = %(paragraph)s and sentence = %(sentence)s and 
index_in_sentence = %(word)s;'''

COUNT_CHARS_IN_SENTENCE = '''select sum(length)
from public."Word_in_Speech" as a
inner join public."Word" as b on a.word_id = b.word_id
Where speech_id = %(speech_id)s and paragraph = %(paragraph)s and sentence = %(sentence)s;'''

COUNT_CHARS_IN_PARAGRAPH = '''select sum(length)
from public."Word_in_Speech" as a
inner join public."Word" as b on a.word_id = b.word_id
Where speech_id = %(speech_id)s and paragraph = %(paragraph)s;'''

COUNT_CHARS_IN_SPEECH = '''select sum(length)
from public."Word_in_Speech" as a
inner join public."Word" as b on a.word_id = b.word_id
Where speech_id = %(speech_id)s;'''

COUNT_WORDS_IN_SENTENCE = '''select count(*)
from public."Word_in_Speech"
Where speech_id = %(speech_id)s and paragraph = %(paragraph)s and sentence = %(sentence)s;'''

COUNT_WORDS_IN_PARAGRAPH = '''select count(*)
from public."Word_in_Speech"
Where speech_id = %(speech_id)s and paragraph = %(paragraph)s;'''

COUNT_WORDS_IN_SPEECH = '''select count(*)
from public."Word_in_Speech"
Where speech_id = %(speech_id)s;'''

WORD_APPEARANCES = '''select a.word_id, word, count(*) as amount
from public."Word" as a
inner join public."Word_in_Speech" as b on a.word_id = b.word_id
group by a.word_id, word
order by amount desc'''

WORD_APPEARANCES_IN_SPEECH = '''select a.word_id, word, count(*) as amount
from public."Word" as a
inner join public."Word_in_Speech" as b on a.word_id = b.word_id
where speech_id = %(speech_id)s
group by a.word_id, word
order by amount desc'''