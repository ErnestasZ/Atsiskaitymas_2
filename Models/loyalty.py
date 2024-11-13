from app import db
from datetime import datetime


class Loyalty(db.Model):
    __tablename__ = 'loyalties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    discount = db.Column(db.Float)
    created_at = db.Column(db.Date, default=datetime.now())
    users = db.relationship('User', back_populates='loyalty')
