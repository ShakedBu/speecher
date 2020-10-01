from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt import JWT
import datetime

from src.Routes.group import Group
from src.Routes.phrase import Phrase
from src.Routes.speech import Speech
from src.Routes.word import Word
from src.Routes.statistics import Statistics
from src.Routes.auth import authenticate, identity # Login, Logout


app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'sh@kedBe$t'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(minutes=15)
jwt = JWT(app, authenticate, identity)

api.add_resource(Word, '/word')
api.add_resource(Phrase, '/phrase')
api.add_resource(Group, '/group')
api.add_resource(Speech, '/speech')
api.add_resource(Statistics, '/statistics')
