from app import create_app, db
from app.models import User

app = create_app()

# 首先导入db 和 User
# 加入到上下文shell中
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}