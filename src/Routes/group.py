from flask_restful import Resource
from flask import request

from src.DBUtils import execute_query, execute_query_safe
from src.queries import NEW_GROUP, GET_WORD, ADD_WORD_TO_GROUP, SEARCH_GROUP, GET_GROUP, DELETE_WORD_FROM_GROUP, \
    GET_ALL_GROUPS


class Group(Resource):
    def get(self):
        if 'id' in request.args:
            return get_group(request.args['id'])

        elif 'query' in request.args:
            return search_groups(request.args['query'])

    def post(self):
        data = request.get_json()
        create_new_group(data['name'], data['words'])

    def put(self):
        data = request.get_json()
        if data['action'] == 'remove':
            remove_words_from_group(data['id'], data['words'])
        else:
            add_words_to_group(data['id'], data['words'])


def create_new_group(name, words):
    group = execute_query_safe(NEW_GROUP, {'group_name': name}, True, True)
    group_id = group[0]

    # Add words to group
    for curr_word in words:
        # Get word
        word = execute_query_safe(GET_WORD, {'word': curr_word}, True, True)

        # Add to group
        execute_query_safe(ADD_WORD_TO_GROUP, {'group_id': group_id, 'word_id': word[0]})

    return group_id


def search_groups(query):
    results = []

    if query != "":
        sql_query = '%' + query + '%'
        groups = execute_query_safe(SEARCH_GROUP, {'query': query}, True)
    groups = execute_query_safe(GET_ALL_GROUPS, is_fetch=True)

    for group in groups:
        results.append({'id': group[0], 'name': group[1]})

    return results


def get_group(group_id):
    results = []
    words = execute_query_safe(GET_GROUP, {'group_id': group_id}, True)

    for word in words:
        results.append({'id': word[0], 'word': word[1].strip()})

    return results


def add_words_to_group(group_id, words):
    for word in words:
        execute_query_safe(ADD_WORD_TO_GROUP, {'group_id': group_id, 'word_id': word})


def remove_words_from_group(group_id, words):
    for word in words:
        execute_query_safe(DELETE_WORD_FROM_GROUP,  {'group_id': group_id, 'word_id': word})
