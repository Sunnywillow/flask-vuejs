from flask import Blueprint

bp = Blueprint('api', __name__) # 创建主蓝本bp名称为api

# 写在最后是为了防止循环导入，ping.py文件也会导入 bp
from app.api import ping

