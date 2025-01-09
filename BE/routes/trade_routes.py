from flask import Blueprint, jsonify, request
from models.trade import Trade
from app import db

trade_routes = Blueprint('trade_routes', __name__)

@trade_routes.route('/propose', methods=['POST'])
def propose_trade():
    data = request.json
    new_trade = Trade(
        initiator=data['initiator'],
        recipient=data['recipient'],
        money_offer=data.get('money_offer', 0),
        money_request=data.get('money_request', 0),
        properties_offer=data.get('properties_offer', []),
        properties_request=data.get('properties_request', [])
    )
    db.session.add(new_trade)
    db.session.commit()
    return jsonify(new_trade.__dict__), 201

@trade_routes.route('/<int:trade_id>/accept', methods=['POST'])
def accept_trade(trade_id):
    trade = Trade.query.get_or_404(trade_id)
    trade.status = 'accepted'
    db.session.commit()
    return jsonify({'message': 'Trade accepted.'})

@trade_routes.route('/<int:trade_id>/reject', methods=['POST'])
def reject_trade(trade_id):
    trade = Trade.query.get_or_404(trade_id)
    trade.status = 'rejected'
    db.session.commit()
    return jsonify({'message': 'Trade rejected.'})