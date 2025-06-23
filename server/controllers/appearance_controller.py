from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity # For JWT protection
from sqlalchemy.exc import IntegrityError

# Import db from config.py
from config import db
from models.appearance import Appearance
from models.guest import Guest # Needed to check guest existence
from models.episode import Episode # Needed to check episode existence


class AppearanceListResource(Resource):
    @jwt_required() # Protect this route with JWT
    def post(self):
        data = request.get_json()
        rating = data.get('rating')
        guest_id = data.get('guest_id')
        episode_id = data.get('episode_id')

        # Basic validation for presence
        if rating is None or guest_id is None or episode_id is None:
            return {'message': 'Rating, guest_id, and episode_id are required'}, 400

        # Validate rating range and type
        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                return {'message': 'Rating must be an integer between 1 and 5'}, 400
        except ValueError:
            return {'message': 'Rating must be an integer'}, 400

        # Check if guest and episode exist
        guest = Guest.query.get(guest_id)
        episode = Episode.query.get(episode_id)

        if not guest:
            return {'message': 'Guest not found'}, 404
        if not episode:
            return {'message': 'Episode not found'}, 404

        try:
            new_appearance = Appearance(
                rating=rating,
                guest_id=guest_id,
                episode_id=episode_id
            )
            db.session.add(new_appearance)
            db.session.commit()
            return new_appearance.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Integrity error. Check foreign keys or unique constraints.'}, 422
        except ValueError as e:
            db.session.rollback()
            return {'message': str(e)}, 400 # For model validation errors
        except Exception as e:
            db.session.rollback()
            return {'message': f'An unexpected error occurred: {str(e)}'}, 500
