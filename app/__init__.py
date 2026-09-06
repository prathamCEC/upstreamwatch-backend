import os
from dotenv import load_dotenv
from flask import Flask
from app.extensions import db, migrate
from app.routes.github import github_bp
from app.routes.repositories import repositories_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    db.init_app(app)
    migrate.init_app(app,db)

    from app import models

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(github_bp)
    app.register_blueprint(repositories_bp)



    return app