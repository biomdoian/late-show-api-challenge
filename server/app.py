from flask import request, make_response, jsonify, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
load_dotenv()

# Import app, db, api, and jwt from config.py
from config import app, api, jwt # Removed db from this import

# Import db from models.__init__.py
from models.__init__ import db

# Import models 
from models.user import User
from models.guest import Guest
from models.episode import Episode
from models.appearance import Appearance

# Import controllers
from controllers.auth_controller import Register, Login
from controllers.guest_controller import GuestListResource # Only list required
from controllers.episode_controller import EpisodeListResource, EpisodeResource # List and single resource
from controllers.appearance_controller import AppearanceListResource # Only post required

# Base Route
@app.route('/')
def index():
    return '<h1>Late Show API</h1>'

#Register API Resources 
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(GuestListResource, '/guests')
api.add_resource(EpisodeListResource, '/episodes')
api.add_resource(EpisodeResource, '/episodes/<int:id>') # For GET and DELETE on single episode
api.add_resource(AppearanceListResource, '/appearances') # For POSTing new appearances

#Error Handlers 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'errors': ['Not Found']}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'errors': ['Bad Request']}), 400)

@app.errorhandler(IntegrityError)
def handle_integrity_error(error):
    db.session.rollback()
    return make_response(jsonify({'errors': ['Integrity Error: A record with this unique value already exists or a foreign key constraint was violated.']}), 422)

@app.errorhandler(Exception)
def handle_exception(e):
    db.session.rollback()
    return make_response(jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500)

#Run App
if __name__ == '__main__':
    app.run(port=5555, debug=True)
