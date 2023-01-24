from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from app.models.user import User
    from app.models.skill import Skill
    from app.models.trade import Trade

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    # from .user_routes import user_bp
    # app.register_blueprint(user_bp)

    # from .skill_routes import skill_bp
    # app.register_blueprint(skill_bp)

    # from .trade_routes import trade_bp
    # app.register_blueprint(trade_bp)

    CORS(app)
    return app