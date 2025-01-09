from flask import Blueprint, jsonify, request
from models.auction import Auction
from app import db

auction_routes = Blueprint('auction_routes', __name__)

@auction_routes.route('/start', methods=['POST'])
def start_auction():
    data = request.json
    new_auction = Auction(
        property_id=data['property_id']
    )
    db.session.add(new_auction)
    db.session.commit()
    return jsonify(new_auction.__dict__), 201

@auction_routes.route('/<int:auction_id>/bid', methods=['POST'])
def place_bid(auction_id):
    auction = Auction.query.get_or_404(auction_id)
    data = request.json
    if auction.place_bid(data['bidder_id'], data['amount']):
        db.session.commit()
        return jsonify({'message': 'Bid placed successfully.'})
    return jsonify({'error': 'Bid too low.'}), 400