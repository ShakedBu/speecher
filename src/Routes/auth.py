from flask_jwt import current_identity
from flask_restful import abort
from functools import wraps


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'speecher', 'test'),
    User(2, 'speecher2', 'test'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user:
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


def check_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_identity.username == 'test':
            return func(*args, **kwargs)
        return abort(401)
    return wrapper
