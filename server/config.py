from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api
from sqlalchemy import MetaData
import os # Import os to get environment variables

app = Flask(__name__)

    # Configure PostgreSQL Database URI
    # IMPORTANT: Replace <user> and <password> with your PostgreSQL username and password.
    # If running locally, it's typically your OS username and a password you set.
    # This should ideally be in a .env file for production.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "postgresql://<user>:<password>@localhost:5432/late_show_db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False # For pretty-printing JSON responses

    # Secret key for Flask sessions and JWT token signing
    # Generate a strong key with `python -c 'import os; print(os.urandom(24))'`
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key_for_dev')
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret_key_for_dev')


    # Setup SQLAlchemy with naming conventions
metadata = MetaData(naming_convention={
        "fk": "fk_%(table_name)s_%(column_names)s_%(referred_table_name)s",
    })
db = SQLAlchemy(metadata=metadata) # Initialize db with metadata
db.init_app(app) # Bind db to the Flask app instance

migrate = Migrate(app, db) # Initialize Flask-Migrate
jwt = JWTManager(app) # Initialize Flask-JWT-Extended
api = Api(app) # Initialize Flask-RESTful API
    