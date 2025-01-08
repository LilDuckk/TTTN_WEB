from app import db

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(50))
    group = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2), default=0.00)
    baserent = db.Column(db.Numeric(10, 2), default=0.00)
    rent1 = db.Column(db.Numeric(10, 2), default=0.00)
    rent2 = db.Column(db.Numeric(10, 2), default=0.00)
    rent3 = db.Column(db.Numeric(10, 2), default=0.00)
    rent4 = db.Column(db.Numeric(10, 2), default=0.00)
    rent5 = db.Column(db.Numeric(10, 2), default=0.00)
    owner_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    mortgaged = db.Column(db.Boolean, default=False)
    houses = db.Column(db.Integer, default=0)
    hotel = db.Column(db.Boolean, default=False)
    houseprice = db.Column(db.Numeric(10, 2), default=0.00)
    landcount = db.Column(db.Integer, default=0)

    def calculate_rent(self):
        if self.hotel:
            return self.rent5
        return [self.baserent, self.rent1, self.rent2, self.rent3, self.rent4][self.houses]

    def __repr__(self):
        return f'<Property {self.name}>'