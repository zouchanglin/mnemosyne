from flask import Blueprint, request, g, current_app

from business.collect_word import get_word
from unity_response import UnityResponse
from business.utils.common_tools import is_english, is_chinese
from business.models import Word

WordCore = Blueprint('WordCore', __name__, url_prefix="/api/word")


@WordCore.route('/search', methods=['POST'])
def search():
    content = request.json['content']
    limit = request.json['limit']
    offset = request.json['offset']
    current_app.logger.info(content)

    if content == "":
        current_app.logger.info('空条件')
        return UnityResponse.success(data={
            "list": Word.query.limit(limit).offset(offset).all()
        })
    else:
        content = content.lower()

    if is_english(content):
        ret = Word.query.filter(Word.word.like('%' + content + '%')).limit(limit).all()
    elif is_chinese(content):
        ret = Word.query.filter(Word.trans.like('%' + content + '%')).limit(limit).all()
    else:
        current_app.logger.info('未知语言')
        return UnityResponse.error(msg='未知语言')
    return UnityResponse.success(data={
        "list": ret
    })


@WordCore.route('/get', methods=['POST'])
def get_one_word():
    word_txt = request.json['word']
    word_txt = word_txt.lower()
    return UnityResponse.success(data=get_word(word_txt))
