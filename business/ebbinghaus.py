from flask import Blueprint, request, g, current_app

from business.services.ebbinghaus_service import (
    learned_or_forget_word_once,
    get_now_need_revise_words
)

from business.services.word_study_service import get_today_study_words

from unity_response import UnityResponse

Ebbinghaus = Blueprint('Ebbinghaus', __name__, url_prefix="/api/ebbinghaus")


@Ebbinghaus.route('/once', methods=['POST'])
def pass_once():
    user_id = g.user_id
    action = request.json['action']
    word_id = request.json['word_id']
    current_app.logger.info('user_id = ', user_id, 'action = ', action, 'word_id = ', word_id)
    learned_or_forget_word_once(word_id, user_id, action)
    return UnityResponse.success(msg='操作成功')


@Ebbinghaus.route('/revise', methods=['POST'])
def revise_word():
    """
    复习单词
    :return:
    """
    user_id = g.user_id
    current_app.logger.info('user_id =%s', user_id)
    words = get_now_need_revise_words(user_id=user_id, strict_mode=False)
    return UnityResponse.success(msg='操作成功', data=words)


@Ebbinghaus.route('/study', methods=['POST'])
def study_word():
    """
    学习新单词
    :return:
    """
    user_id = g.user_id
    current_app.logger.info('user_id =%s', user_id)
    words = get_today_study_words(user_id=user_id)
    return UnityResponse.success(msg='操作成功', data=words)


@Ebbinghaus.route('/import', methods=['POST'])
def import_words():
    user_id = g.user_id
    current_app.logger.info('user_id =%s', user_id)
    word_ids = request.json['word_ids']
    for word_id in word_ids:
        learned_or_forget_word_once(word_id, user_id, True)
    return UnityResponse.success(msg='操作成功')
