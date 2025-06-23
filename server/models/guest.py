from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Import db from config.py
from config import db


class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define one-to-many relationship with Appearance
    appearances = relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    # Serialization rules: Prevent recursion
    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f'<Guest {self.id}: {self.name} ({self.occupation})>'

    # --- Validation for Guest model ---
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Guest name must be present.")
        return name