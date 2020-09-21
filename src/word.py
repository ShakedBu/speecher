from src.DBUtils import execute_query
from .queries import GET_ALL_WORDS


def get_all_words():
    results = []
    words = execute_query(GET_ALL_WORDS, True)

    for word in words:
        results.append({'id': word[0], 'word': word[1].strip()})

    return results
