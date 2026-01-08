from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.import_routes import import_bp
    from app.routes.image_routes import image_bp
    
    app.register_blueprint(import_bp, url_prefix='/api')
    app.register_blueprint(image_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
