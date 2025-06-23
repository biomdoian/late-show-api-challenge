from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Import db from config.py
from config import db


class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define one-to-many relationship with Appearance
    appearances = relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')

    # Serialization rules: Prevent recursion
    serialize_rules = ('-appearances.episode',)

    def __repr__(self):
        return f'<Episode {self.id}: {self.date} (No. {self.number})>'

    # --- Validation for Episode model ---
    @validates('number')
    def validate_number(self, key, number):
        if not isinstance(number, int) or number <= 0:
            raise ValueError("Episode number must be a positive integer.")
        return number

    @validates('date')
    def validate_date(self, key, date):
        # Basic type check; more robust date validation (e.g., format) would be done at API input
        if not isinstance(date, datetime) and not isinstance(date, type(None)):
            try:
                date = datetime.strptime(str(date), '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Episode date must be a valid date format (YYYY-MM-DD).")
        return date
