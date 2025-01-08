from app import db

class Auction(db.Model):
    __tablename__ = 'auctions'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    highest_bid = db.Column(db.Numeric(10, 2), default=0.00)
    highest_bidder = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    current_bidder = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    status = db.Column(db.String(50), default='ongoing')

    def place_bid(self, bidder_id, amount):
        if amount > self.highest_bid:
            self.highest_bid = amount
            self.highest_bidder = bidder_id
            return True
        return False

    def __repr__(self):
        return f'<Auction Property {self.property_id}>'