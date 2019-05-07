from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    # 对当前用户调用get_token()方法，[其中进行下面两步后]赋值给token
    token = g.current_user.get_token()
    # 提交到数据库
    db.session.commit()
    # 将令牌json化`
    return jsonify({'token': token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204

