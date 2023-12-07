from flask import Blueprint, request, g, current_app

from unity_response import UnityResponse
from business.utils.common_tools import is_english, is_chinese, get_now_time
from business.vo.word_detail import WordDetail
from business.vo.word_vo import WordVO
from database import db
from business.models import Word, UserWord


WordCore = Blueprint('WordCore', __name__, url_prefix="/api/word")


@WordCore.route('/learned', methods=['POST'])
def learned():
    sid = request.json['id']
    action = request.json['action']
    # 从全局变量获取
    user_id = g.user_id
    ret = UserWord.query.filter_by(word_id=sid, user_id=user_id).first()
    if ret is None:
        data = UserWord()
        data.word_id = sid
        data.user_id = user_id
        data.learned = action
        db.session.add(data)
    else:
        ret.update_time = get_now_time()
        ret.learned = action
    db.session.commit()
    return UnityResponse.success(msg='操作成功')


@WordCore.route('/search', methods=['POST'])
def search():
    content = request.json['content']
    limit = request.json['limit']
    offset = request.json['offset']
    current_app.logger.info(content)

    if content == "":
        current_app.logger.info('空条件')
        return UnityResponse.success(data={
            "list": [WordVO.word_2_vo(r) for r in Word.query.limit(limit).offset(offset).all()]
        })

    # 查找包含content的词
    # ret = Word.query.filter(Word.word.like('%' + content + '%')).limit(limit).all()
    if is_english(content):
        ret = Word.query.filter(Word.word.like('%' + content + '%')).limit(limit).all()
    elif is_chinese(content):
        ret = Word.query.filter(Word.trans_cn.like('%' + content + '%')).limit(limit).all()
    else:
        current_app.logger.info('未知语言')
        return UnityResponse.error(msg='未知语言')
    return UnityResponse.success(data={
        "list": [WordVO.word_2_vo(r) for r in ret]
    })


# flask 统一 request.headers.get('Authorization')
@WordCore.route('/detail', methods=['POST'])
def detail():
    sid = request.json['id']
    ret = Word.query.filter(Word.id == sid).first()
    if ret:
        detail_vo = WordDetail.word_2_vo(ret)
        pd = UserWord.query.filter_by(word_id=sid, user_id=g.user_id).first()
        if pd:
            detail_vo.learned = pd.learned
            detail_vo.killed = pd.killed
            detail_vo.error_count = pd.error_count
            detail_vo.pitch_count = pd.pitch_count
        return UnityResponse.success(data=detail_vo)
    else:
        return UnityResponse.error(msg='未找到该单词')


@WordCore.route('/killed', methods=['POST'])
def killed():
    sid = request.json['id']
    action = request.json['action']
    # 从全局变量获取
    user_id = g.user_id
    ret = UserWord.query.filter_by(word_id=sid, user_id=user_id).first()
    if ret is None:
        data = UserWord()
        data.word_id = sid
        data.user_id = user_id
        data.learned = True
        data.killed = action
        db.session.add(data)
    else:
        ret.killed = action
        ret.update_time = get_now_time()
    db.session.commit()
    return UnityResponse.success(msg='操作成功')
