from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy import inspect # Used for username validation logic

# Import db and bcrypt from config.py
from config import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Serialization rules: Prevent _password_hash from being exposed
    serialize_rules = ('-_password_hash',)

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

    # Password Hashing with Flask-Bcrypt 
    @property
    def password_hash(self):
        raise AttributeError('Password hashes cannot be read.')

    @password_hash.setter
    def password_hash(self, password):
        from config import bcrypt # Local import to avoid circular dependency
        self._password_hash = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')

    def authenticate(self, password):
        from config import bcrypt # Local import
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    #Validation for User model 
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must be present.")
        
        if inspect(self).persistent: 
            original_username = self._sa_instance_state.original_state.get('username')
            if original_username != username and User.query.filter_by(username=username).first():
                raise ValueError("Username must be unique.")
        else:
            if User.query.filter_by(username=username).first():
                raise ValueError("Username must be unique.")
        
        return username