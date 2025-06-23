from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
import datetime

# Import db and app from config.py
from config import db, app, bcrypt # Import bcrypt for password hashing
from models.user import User

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        try:
            # Create a new user instance
            new_user = User(username=username)
            # Use the password_hash setter to hash the password
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User registered successfully'}, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Username already exists'}, 409
        except ValueError as e:
            db.session.rollback()
            return {'message': str(e)}, 422 # For validation errors

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            # Create a JWT token that expires in 1 hour
            access_token = create_access_token(
                identity=user.id,
                expires_delta=datetime.timedelta(hours=1)
            )
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
