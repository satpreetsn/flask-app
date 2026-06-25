import os
from config_loader import load_config

config_data = load_config()

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_engine_options():
        db_config = config_data["database"]

        return {
            "pool_size": db_config["pool_size"],
            "max_overflow": db_config["max_overflow"],
            "pool_timeout": db_config["pool_timeout"],
            "pool_recycle": db_config["pool_recycle"],
            "pool_pre_ping": db_config["pool_pre_ping"]
        }


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class CloudConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config_map = {
    "dev": DevConfig,
    "cloud": CloudConfig
}