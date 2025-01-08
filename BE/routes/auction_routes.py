from flask import Blueprint, jsonify, request
from models.auction import Auction

auction_routes = Blueprint('auction_routes', __name__)

# Danh sách đấu giá tạm thời
auctions = {}

@auction_routes.route('/start', methods=['POST'])
def start_auction():
    data = request.json
    property_id = data['property_id']
    bidders = data['bidders']
    auction = Auction(property_id=property_id)
    auction.bidders = bidders
    auctions[property_id] = auction
    return jsonify({'message': f'Auction started for property {property_id}.'}), 201

@auction_routes.route('/bid/<int:property_id>', methods=['POST'])
def place_bid(property_id):
    data = request.json
    bidder_id = data['bidder_id']
    bid_amount = data['bid_amount']

    if property_id not in auctions:
        return jsonify({'error': 'Auction not found.'}), 404

    auction = auctions[property_id]

    try:
        auction.place_bid(bidder_id, bid_amount)
        return jsonify({'message': 'Bid placed successfully.', 'highest_bid': auction.highest_bid})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@auction_routes.route('/pass/<int:property_id>', methods=['POST'])
def pass_turn(property_id):
    data = request.json
    bidder_id = data['bidder_id']

    if property_id not in auctions:
        return jsonify({'error': 'Auction not found.'}), 404

    auction = auctions[property_id]
    winner = auction.pass_turn(bidder_id)

    if winner is not None:
        return jsonify({'message': f'Auction ended. Winner: Player {winner}', 'property_id': property_id})
    return jsonify({'message': 'Turn passed.'})
