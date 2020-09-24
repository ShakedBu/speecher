from src.DBUtils import execute_query
from src.queries import GET_ALL_COUNTS


def get_general_counts_by_speech(speech_id):
    results = []
    counts = execute_query(GET_ALL_COUNTS.format(speech_id), True)

    for count in counts:
        results.append({'paragraph': count[0], 'sentence': count[1], 'words': count[2]})

    return results
