from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String)
    veryfied_at = db.Column(db.Date)
    is_deleted = db.Column(db.Boolean, default=False)
    # uzduotyje parasyta per tam tikra laika
    blocked_until = db.Column(db.Date)
    failed_count = db.Column(db.Integer)
    loyalty_id = db.Column(db.Integer, db.ForeignKey('loyalties.id'))
    loyalty = db.relationship('Loyalty', back_populates='users')
