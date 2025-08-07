from flask import Flask
from app.routes.resume_routes import resume_bp
from app.routes.rag_routes import qa_bp
from .extensions import db, ma, cors
from flask_jwt_extended import JWTManager
from .config import Config

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)
    jwt.init_app(app)
    
    app.register_blueprint(resume_bp, url_prefix="/resume")
    app.register_blueprint(qa_bp, url_prefix="/qa")
    
    with app.app_context():
        db.create_all()
    return app
