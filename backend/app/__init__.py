from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 注册api蓝本
    from app.api import bp as api_bp  # 从api中导入实例bp
    app.register_blueprint(api_bp, url_prefix='/api') # 注册

    return app
