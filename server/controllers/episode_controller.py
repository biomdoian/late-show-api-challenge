from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity # For JWT protection
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Import db from config.py
from config import db
from models.episode import Episode
from models.appearance import Appearance # Needed for relationship access

class EpisodeListResource(Resource):
    def get(self):
        episodes = Episode.query.all()
        # If full appearances are needed, iterate and use .to_dict() with serialize_rules
        return [episode.to_dict() for episode in episodes], 200

class EpisodeResource(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return {'message': 'Episode not found'}, 404
        
        # The serialize_rules on Episode will handle appearances serialization
        return episode.to_dict(), 200

    @jwt_required() # Protect this route with JWT
    def delete(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return {'message': 'Episode not found'}, 404

        try:
            # Due to cascade='all, delete-orphan' in Episode model,( deleting the episode will automatically delete associated appearances.)
            db.session.delete(episode)
            db.session.commit()
            return {'message': 'Episode and associated appearances deleted successfully'}, 204 # 204 No Content for successful deletion
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting episode: {str(e)}'}, 500
