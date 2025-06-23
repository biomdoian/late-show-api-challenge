from flask import request, make_response, jsonify, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
    
    # Import app, db, api, and jwt from config.py
from config import app, db, api, jwt # Ensure jwt is imported
    
    # Import models (will be populated in next step)
    # from models.user import User
    # from models.guest import Guest
    # from models.episode import Episode
    # from models.appearance import Appearance
    
    # --- Base Route ---
@app.route('/')
def index():
    return '<h1>Late Show API</h1>'
    
    # --- Define API Resources (Classes will be implemented in controllers later) ---
    # Placeholder classes for now, just for API resource registration
class UserResource(Resource):
    pass
class GuestListResource(Resource):
    pass
class EpisodeListResource(Resource):
    pass
class AppearanceListResource(Resource):
    pass
    
    # --- Register API Resources ---
    # These will be implemented fully in controllers in later phases
api.add_resource(UserResource, '/users') # Example for user-related ops
api.add_resource(GuestListResource, '/guests')
api.add_resource(EpisodeListResource, '/episodes')
api.add_resource(AppearanceListResource, '/appearances')
    
    # --- Error Handlers (Good practice for APIs) ---
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
        # General error handler for unhandled exceptions
    db.session.rollback() # Rollback in case of database error
    return make_response(jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500)

    # --- Run App ---
if __name__ == '__main__':
    app.run(port=5555, debug=True)

    