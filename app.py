from flask import Flask, jsonify
from flask.ext.restful import Api, Resource, reqparse

import os
import random
import string

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
api = Api(app)

decks = {}


class Card(object):
    """docstring for Card"""

    def __init__(self):
        super(Card, self).__init__()
        self.ID = 0
        self.rating = 0
        self.type = 0
        self.question = ""
        self.answer = ""
        self.false_answer = ""


def parse_card(**args):
    card = Card()
    try:
        card.ID = args['ID']
        card.rating = args['rating']
        card.type = args['type']
        card.question = args['question']
        card.answer = args['answer']
        card.false_answer = args['false_answer']

    except KeyError:
        raise TypeError("invalid args")

    return card


def card_to_dict(card):
    return {'ID': card.ID,
            'rating': card.rating,
            'type': card.type,
            'question': card.question,
            'answer': card.answer,
            'false_answer': card.false_answer}


def parse_cards(value):
    cards = []
    try:
        for v in value:
            card = parse_card(**v)
            cards.append(card)
    except TypeError:
        raise ValueError("Invalid Card")

    return cards


class Deck(object):
    """docstring for Deck"""

    def __init__(self, ID, name, cards):
        super(Deck, self).__init__()
        self.ID = ID
        self.name = name
        self.cards = cards


def deck_to_dict(deck):
    return {'name': deck.name,
            'cards': [card_to_dict(card) for card in deck.cards]}


def random_id():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(16))


def deck_parser():
    deck_parse = reqparse.RequestParser()
    deck_parse.add_argument('name', type=str, required=True, location='json')
    deck_parse.add_argument(
        'cards', type=parse_cards, required=True, location='json')

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
    decks[id] = deck

    return id


@app.route('/deck/<string:id>', methods=['GET'])
def get_deck_entry(id):
    try:
        deck = decks[id]
    except KeyError:
        return "deck not found", 404

    return jsonify(deck_to_dict(deck))


@app.route('/deck/<string:id>', methods=['PUT'])
def update_deck_entry(id):
    args = deck_parser().parse_args()
    deck = Deck(id, args['name'], args['cards'])
    decks[id] = deck

    return jsonify(deck_to_dict(deck))


if __name__ == '__main__':
    app.run()
