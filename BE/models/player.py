from app import db

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    position = db.Column(db.Integer, default=0)
    money = db.Column(db.Numeric(10, 2), default=1500.00)
    creditor = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    jail = db.Column(db.Boolean, default=False)
    jail_roll = db.Column(db.Integer, default=0)
    community_chest_card = db.Column(db.Boolean, default=False)
    chance_card = db.Column(db.Boolean, default=False)

    def pay(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        else:
            return False

    def receive(self, amount):
        self.money += amount

    def __repr__(self):
        return f'<Player {self.name}>'