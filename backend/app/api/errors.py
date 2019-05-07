from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from app import db
from app.api import bp


def error_response(status_code, message=None):
    # 核心
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message  # 加入message
    response = jsonify(payload)
    # 估计是方便维护，增加response的status_code属性
    response.status_code = status_code
    return response


def bad_request(message):
    '''最常用的错误400： 错误的请求'''
    return error_response(400, message)


@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)