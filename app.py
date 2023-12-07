import logging
import os

from flask import render_template, request, g
from flask_cors import CORS

import log_handler
from run import app
from unity_response import UnityResponse
from database import db
from business.models import Base, User

# 添加日志配置
logHandler = log_handler.get_log_handler()
app.logger.addHandler(logHandler)

# 配置数据库(develop)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# 配置数据库(production)

print(os.environ.get('MYSQL_URL'))
print(os.environ.get('OPENAI_API_KEY'))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MYSQL_URL')

# allow all origins
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template('index.html')


@app.before_request
def auth_token():
    ignore_list = ['/',
                   '/api/auth/login',
                   '/api/auth/register',
                   '/api/log/sse',
                   '/api/ping/sse']
    if request.path in ignore_list:
        return
    else:
        try:
            find_ret = User.query.filter_by(id=request.headers.get('Authorization')).first()
            if find_ret is None:
                return UnityResponse.error(msg='无效token', code=-1)
            else:
                # token有效的情况
                g.user_id = find_ret.id
                # setattr(g, 'user_id', find_ret.id)
        except Exception as e:
            app.logger.info(e)
            return UnityResponse.error(msg='token获取失败', code=-1)


@app.errorhandler(Exception)
def error_handler(e):
    """
    全局异常捕获，也相当于一个视图函数
    """
    logging.exception(e)
    return UnityResponse.error(msg=str(e))


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        Base.metadata.create_all(db.engine)
        app.logger.info('数据库初始化成功')
    from business.user_authorize import Authorize
    from business.word_list import WordCore
    from business.article_study import ArticleCore
    from business.embedding.vector_tools import WordVector
    from business.ebbinghaus import Ebbinghaus
    from business.log.log_sse import LogSSE
    from business.log.ping_sse import PingSSE

    app.register_blueprint(Authorize)
    app.register_blueprint(WordCore)
    app.register_blueprint(ArticleCore)
    app.register_blueprint(WordVector)
    app.register_blueprint(Ebbinghaus)
    app.register_blueprint(LogSSE)
    app.register_blueprint(PingSSE)
    app.run(host='0.0.0.0', port=5005, debug=False)
