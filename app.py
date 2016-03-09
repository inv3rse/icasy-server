from flask import Flask, jsonify
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

import os
import random
import string

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
api = Api(app)


class Deck(db.Model):
    """docstring for Deck"""

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    cards = db.Column(JSON)

    def __init__(self, id, name, cards):
        super(Deck, self).__init__()
        self.id = id
        self.name = name
        self.cards = cards


def deck_to_dict(deck):
    return {'name': deck.name,
            'cards': deck.cards}


def random_id():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(16))


def deck_parser():
    deck_parse = reqparse.RequestParser()
    deck_parse.add_argument('name', type=str, required=True, location='json')
    deck_parse.add_argument('cards', type=str, required=True, location='json')

    return deck_parse


class DecksApi(Resource):
    """docstring for DecksApi"""

    def __init__(self, arg):
        super(DecksApi, self).__init__()
        self.arg = arg


@app.route('/deck', methods=['POST'])
def create_deck_entry():
    args = deck_parser().parse_args()
    id = random_id()
    deck = Deck(id, args['name'], args['cards'])
    db.session.add(deck)
    db.session.commit()

    return id


@app.route('/deck/<string:id>', methods=['GET'])
def get_deck_entry(id):
    deck = db.session.query(Deck).get(id)
    if deck is None:
        return "deck not found", 404

    return jsonify(deck_to_dict(deck))


@app.route('/deck/<string:id>', methods=['PUT'])
def update_deck_entry(id):
    deck = db.session.query(Deck).get(id)
    if deck is None:
        return "deck not found", 404

    args = deck_parser().parse_args()
    deck.name = args['name']
    deck.cards = args['cards']

    db.session.commit()

    return jsonify(deck_to_dict(deck))


if __name__ == '__main__':
    app.run()
