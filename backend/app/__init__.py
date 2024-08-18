from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from flask_session import Session
import secrets
import os

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Generate and set the secret key
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    
    # Configure session to use filesystem (default is cookies)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'obster_'
    app.config['SESSION_FILE_DIR'] = '/tmp/flask_session/'  # Add this line to specify session file directory

    # Ensure the session directory exists
    session_dir = app.config['SESSION_FILE_DIR']
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})
    
    Session(app)  # Initialize the session with the app

    with app.app_context():
        from . import routes
        routes.init_app(app)
        db.create_all()

    return app
