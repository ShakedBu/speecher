from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity

from src.Routes.group import Group
from src.Routes.phrase import Phrase
from src.Routes.speech import Speech
from src.Routes.word import Word
from src.Routes.statistics import Statistics
from src.Routes.auth import authenticate, identity # Login, Logout


def create_app():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    app.config['JWT_SECRET_KEY'] = 'sh@kedBe$t'
    jwt = JWT(app, authenticate, identity)

    api.add_resource(Word, '/word')
    api.add_resource(Phrase, '/phrase')
    api.add_resource(Group, '/group')
    api.add_resource(Speech, '/speech')
    api.add_resource(Statistics, '/statistics')

    return app
