import base64
from datetime import datetime, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask import url_for


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码
    # 增加token和token过期时间的属性
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):  # 用户对象转换为JSON对象
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):  # JSON对象转化为User对象
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])  # setattr设置实例的field属性,值为data[field]
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        # now当前时间
        now = datetime.utcnow()
        # 如果令牌存在且令牌国企时间大于now+60s
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            # 调用self.token方法
            return self.token
        # 定义token方法 利用urandom生成随机散列值然后进行b64编码，最后解码为utf-8格式
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        # 更新user实例
        db.session.add(self)
        return self.token

    # token过期时间初始化
    def revoke_token(self):
        # 重新定义token过期时间
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    # 不需要user实例只需要token
    @staticmethod
    def check_token(token):
        # 首先过滤user
        user = User.query.filter_by(token=token).first()
        # 如果用户不存在或令牌过期
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user






