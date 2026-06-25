import os

from flask import Flask
from dotenv import load_dotenv

from config import config_map
from database.db import db
from routes.user_route import user_bp
from routes.health_check import health_bp

def create_app():

    env = os.getenv("APP_ENV", "dev")
    print("Current directory:", os.getcwd())
    print("Exists:", os.path.exists(".env.dev"))

    file_loaded = load_dotenv(f".env.{env}")

    app = Flask(__name__)

    app.config.from_object(config_map[env])
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = (
        config_map[env].get_engine_options()
    )

    print("Exists:", os.getenv("DATABASE_URL"))

    db.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(health_bp)


    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0",
    port=5000,
        debug=os.getenv("DEBUG"))
