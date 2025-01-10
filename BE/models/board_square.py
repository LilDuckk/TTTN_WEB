from app import db

class BoardSquare(db.Model):
    __tablename__ = 'board'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(
        'CITY', 'START', 'TRAIN', 'POWERPLANT', 'SECRET', 
        'PRISON', 'GOTO', 'PARKING', 'FINE'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    build_price = db.Column(db.Numeric(10, 2), nullable=True)
    rent = db.Column(db.JSON, nullable=True)  # Dạng JSON để lưu tiền thuê
    special_action = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<BoardSquare {self.label} (Type: {self.type})>'
