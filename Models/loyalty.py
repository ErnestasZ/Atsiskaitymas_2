from app import db

class Loyalty(db.Model):
    __tablename__ = 'loyalties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # relations
    users = db.relationship('User', back_populates='loyalty')
    def __str__(self) -> str:
        return self.name