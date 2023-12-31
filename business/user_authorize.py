from flask import Blueprint, request, current_app

from business.models import User, UserProfile
from run import app
from unity_response import UnityResponse
from database import db

Authorize = Blueprint('Authorize', __name__, url_prefix="/api/auth")


@Authorize.route('/login', methods=['POST'])
def login():
    """
    用户登录接口
    """
    email = request.json['email']
    password = request.json['password']
    app.logger.info('email = %s, password = %s', email, password)
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return UnityResponse.success(data={
            "nickname": user.nickname,
            "email": user.email,
            "token": user.id,
        })
    else:
        return UnityResponse.error(msg='用户名或密码错误')


@Authorize.route('/register', methods=['POST'])
def register():
    """
    用户注册接口
    """
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user:
        return UnityResponse.error(msg='邮箱已存在')
    else:
        user = User(nickname=email, password=password, email=email)
        db.session.add(user)
        db.session.commit()

        # 新增一个用户配置数据
        db.session.add(UserProfile(user_id=user.id))
        db.session.commit()
        return UnityResponse.success(data={
            "nick_name": user.nickname,
            "token": user.id,
        })
