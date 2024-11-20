from app import db


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    session_id = db.Column(db.String, unique=True, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
