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

    # # Configure application to store JWTs in cookies
    # app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    # # Only allow JWT cookies to be sent over https.
    # # In production, this should likely be True
    # app.config['JWT_COOKIE_SECURE'] = False
    # # Enable csrf double submit protection
    # app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    # Set the secret key to sign the JWTs with
    app.config['JWT_SECRET_KEY'] = 'sh@kedBe$t'
    jwt = JWT(app, authenticate, identity)

    api.add_resource(Word, '/word')
    api.add_resource(Phrase, '/phrase')
    api.add_resource(Group, '/group')
    api.add_resource(Speech, '/speech')
    api.add_resource(Statistics, '/statistics')
    # api.add_resource(Login, '/login')
    # api.add_resource(Logout, '/logout')

    return app
