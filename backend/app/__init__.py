from flask import Flask
from flask_cors import CORS
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Flask-SQLAlchemy plugin
db = SQLAlchemy()
# Flask-Migrate plugin
migrate = Migrate()


def create_app(config_class=Config):   # 定义工厂函数（参数名）
    app = Flask(__name__)             # 实例化app
    app.config.from_object(config_class)

    # enable CORS
    CORS(app)
    # Init Flask-SQLAlchemy
    db.init_app(app)
    # Init Flask-Migrate
    migrate.init_app(app, db)

    # 注册api蓝本
    from app.api import bp as api_bp  # 从api中导入实例bp
    app.register_blueprint(api_bp, url_prefix='/api') # 注册

    return app

from app import models