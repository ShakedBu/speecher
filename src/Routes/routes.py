from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from src.Routes.group import Group
from src.Routes.phrase import Phrase
from src.Routes.speech import Speech
from src.Routes.word import Word
from src.Routes.statistics import Statistics


def create_app():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    api.add_resource(Word, '/word')
    api.add_resource(Phrase, '/phrase')
    api.add_resource(Group, '/group')
    api.add_resource(Speech, '/speech')
    api.add_resource(Statistics, '/statistics')
    # TODO: Extra subject

    return app
