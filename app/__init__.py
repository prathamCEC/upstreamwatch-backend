import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import db
from app.routes.github import github_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    db.init_app(app)

    from app import models 

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    app.register_blueprint(github_bp)

    with app.app_context():
        db.create_all()

    return app