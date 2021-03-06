from flask_restful import Resource
from flask import request, abort
from flask_jwt import jwt_required

from src.DBUtils import execute_query_safe
from src.queries import NEW_GROUP, GET_WORD, ADD_WORD_TO_GROUP, SEARCH_GROUP, GET_GROUP, DELETE_WORD_FROM_GROUP, \
    GET_ALL_GROUPS


class Group(Resource):
    @jwt_required()
    def get(self):
        if 'id' in request.args:
            return get_group(request.args['id'])

        elif 'query' in request.args:
            return search_groups(request.args['query'])

    @jwt_required()
    def post(self):
        data = request.get_json()
        create_new_group(data.get('name'), data.get('words'))

    @jwt_required()
    def put(self):
        data = request.get_json()
        if data['action'] == 'remove':
            remove_words_from_group(data.get('id'), data.get('words'))
        else:
            add_words_to_group(data.get('id'), data.get('words'))


def create_new_group(name, words):
    if name is None:
        abort(400, 'No Group Name given')

    group = execute_query_safe(NEW_GROUP, {'group_name': name}, True, True)

    if group is None:
        abort(500, 'Cannot create group')

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
        groups = execute_query_safe(SEARCH_GROUP, {'query': sql_query}, True)
    else:
        groups = execute_query_safe(GET_ALL_GROUPS, is_fetch=True)

    for group in groups:
        results.append({'id': group[0], 'name': group[1]})

    return results


def get_group(group_id):
    if group_id is None:
        abort(400, 'No Group Id given')

    results = []
    words = execute_query_safe(GET_GROUP, {'group_id': group_id}, True)

    for word in words:
        results.append({'id': word[0], 'word': word[1].strip()})

    return results


def add_words_to_group(group_id, words):
    if group_id is None or words is None:
        abort(400, 'must get group id & word id')

    for word in words:
        response = execute_query_safe(ADD_WORD_TO_GROUP, {'group_id': group_id, 'word_id': word}, True)

    if response is None:
        abort(500, 'Cannot add word to group')


def remove_words_from_group(group_id, words):
    if group_id is None or words is None:
        abort(400, 'must get group id & word id')

    for word in words:
        response = execute_query_safe(DELETE_WORD_FROM_GROUP,  {'group_id': group_id, 'word_id': word}, True)

    if response is None:
        abort(500, 'Cannot remove word from group')
