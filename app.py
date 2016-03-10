from flask import Flask, jsonify, request
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
    data = db.Column(JSON)

    def __init__(self, id, data):
        super(Deck, self).__init__()
        self.id = id
        self.data = data


def random_id():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(16))


@app.route('/deck', methods=['POST'])
def create_deck_entry():
    data = request.get_json()
    id = random_id()
    deck = Deck(id, data)
    db.session.add(deck)
    db.session.commit()

    return id


@app.route('/deck/<string:id>', methods=['GET'])
def get_deck_entry(id):
    deck = db.session.query(Deck).get(id)
    if deck is None:
        return "deck not found", 404

    return jsonify(deck.data)


@app.route('/deck/<string:id>', methods=['PUT'])
def update_deck_entry(id):
    deck = db.session.query(Deck).get(id)
    if deck is None:
        return "deck not found", 404

    data = request.get_json()
    deck.data = data

    db.session.commit()

    return jsonify(deck.data)


if __name__ == '__main__':
    app.run()
