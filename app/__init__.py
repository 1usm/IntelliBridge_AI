from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    
    # Import blueprints
    from app.routes.chatbot_routes import chatbot_bp, main_bp
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(chatbot_bp)
    
    return app