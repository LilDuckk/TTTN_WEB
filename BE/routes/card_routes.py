from flask import Blueprint, jsonify
from models.card import Card
from app import db

card_routes = Blueprint('card_routes', __name__)

@card_routes.route('/draw/<string:deck>', methods=['GET'])
def draw_card(deck):
    card = Card.query.filter_by(type=deck).first()
    if not card:
        return jsonify({'error': 'No cards left in the deck.'}), 404
    db.session.delete(card)
    db.session.commit()
    return jsonify({'text': card.text, 'action': card.action})