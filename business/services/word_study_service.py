"""
单词学习服务
"""
from flask import current_app

from business.models import UserWord, UserProfile, Word
from database import db


def get_today_study_words(user_id: int):
    """
    获得今日要学的新单词
    :param user_id:
    """
    ret_words = []
    # 1. 获取用户今天学习的单词
    ret = UserWord.query.filter(db.cast(UserWord.update_time, db.DATE))
    ret = [i.word_id for i in ret]
    user_profile = UserProfile.query.get(user_id)
    if user_profile:
        day_learn = user_profile.day_learn
        ret_words = Word.query.filter(Word.id.in_(ret)).all()

        # 如果今天学习的单词已经超过了每日学习的单词数量，则不再学习新单词
        if len(ret) < day_learn:
            study_new_num = day_learn - len(ret)
            ret_words.extend(Word.query.filter(~Word.id.in_(ret)).limit(study_new_num).all())
            # TODO 标记这些单词是已经学习过的单词(不过也不急于这一时标记)
    else:
        current_app.logger.error('严重错误: 用户配置数据不存在')
    return ret_words
