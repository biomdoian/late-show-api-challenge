from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Import db from config.py
from config import db


class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Foreign keys to link to Guest and Episode
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)

    # Define many-to-one relationships with Guest and Episode
    guest = relationship('Guest', back_populates='appearances')
    episode = relationship('Episode', back_populates='appearances')

    # Serialization rules: Prevent recursion
    serialize_rules = ('-guest.appearances', '-episode.appearances',)

    def __repr__(self):
        return f'<Appearance {self.id}: Rating {self.rating}>'

    # --- Validation for Appearance model ---
    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        return rating
