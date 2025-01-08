from flask import Blueprint, jsonify, request
from models.card import Card

card_routes = Blueprint('card_routes', __name__)

# Bộ bài tạm thời
chance_cards = [
    Card(1, "Advance to GO. Collect $200.", lambda player: player.receive(200)),
    Card(2, "Pay $50.", lambda player: player.pay(50))
]

community_chest_cards = [
    Card(1, "Get out of Jail Free.", lambda player: setattr(player, 'community_chest_card', True)),
    Card(2, "You have won $100.", lambda player: player.receive(100))
]

@card_routes.route('/draw/<string:deck>', methods=['GET'])
def draw_card(deck):
    if deck == 'chance':
        card = chance_cards.pop(0)
        return jsonify({'card': card.text})
    elif deck == 'community_chest':
        card = community_chest_cards.pop(0)
        return jsonify({'card': card.text})
    return jsonify({'error': 'Invalid deck.'}), 400
