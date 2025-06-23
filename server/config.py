from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api
import os
from flask_bcrypt import Bcrypt # Import Bcrypt

# Import db from models.__init__.py
from models.__init__ import db

app = Flask(__name__)

# Configure PostgreSQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Secret key for Flask sessions and JWT token signing
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')


# Initialize Flask-Migrate with app and db
migrate = Migrate(app, db)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Initialize Flask-RESTful API
api = Api(app)

# Bind db to the Flask app instance
db.init_app(app)