import datetime

from flask import Blueprint, request, g

from unity_response import UnityResponse
from database import db
from business.models import Word, UserWord


ArticleCore = Blueprint('ArticleCore', __name__, url_prefix="/api/article")


@ArticleCore.route('/generate', methods=['POST'])
def generate():
    """
    根据今日学习的单词生成短文
    :return:
    """
    # 从全局变量获取
    # user_id = g.user_id
    user_id = g.user_id
    # 获取今天学习的单词
    ret = UserWord.query.filter(db.cast(UserWord.update_time, db.DATE)
                                == db.cast(datetime.datetime.now(), db.DATE)).all()
    # 查找向量接近词

    return UnityResponse.success(msg='操作成功')
