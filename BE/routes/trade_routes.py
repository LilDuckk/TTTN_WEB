from flask import Blueprint, jsonify, request
from models.trade import Trade

trade_routes = Blueprint('trade_routes', __name__)

# Danh sách giao dịch tạm thời
trades = {}

@trade_routes.route('/propose', methods=['POST'])
def propose_trade():
    data = request.json
    trade = Trade(
        initiator_id=data['initiator_id'],
        recipient_id=data['recipient_id'],
        money_offer=data.get('money_offer', 0),
        money_request=data.get('money_request', 0),
        properties_offer=data.get('properties_offer', []),
        properties_request=data.get('properties_request', [])
    )
    trade_id = len(trades) + 1
    trades[trade_id] = trade
    return jsonify({'message': 'Trade proposed successfully.', 'trade_id': trade_id})

@trade_routes.route('/<int:trade_id>/accept', methods=['POST'])
def accept_trade(trade_id):
    if trade_id not in trades:
        return jsonify({'error': 'Trade not found.'}), 404

    trade = trades[trade_id]
    trade.accept()
    return jsonify({'message': 'Trade accepted.'})

@trade_routes.route('/<int:trade_id>/reject', methods=['POST'])
def reject_trade(trade_id):
    if trade_id not in trades:
        return jsonify({'error': 'Trade not found.'}), 404

    trade = trades[trade_id]
    trade.reject()
    return jsonify({'message': 'Trade rejected.'})
