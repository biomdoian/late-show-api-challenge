from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Import db from config.py
from config import db
from models.guest import Guest

class GuestListResource(Resource):
    def get(self):
        guests = Guest.query.all()
        return [guest.to_dict() for guest in guests], 200

class GuestResource(Resource): # For /guests/<int:id> if needed, though not explicitly in requirements
    def get(self, id):
        guest = Guest.query.get(id)
        if not guest:
            return {'message': 'Guest not found'}, 404
        return guest.to_dict(), 200

   