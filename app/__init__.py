from flask import Flask
from app.routes.resume_routes import resume_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(resume_bp)
    
    # Initialize other extensions (db, JWT, etc.)
    return app
