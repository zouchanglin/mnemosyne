import requests

from business.models import Word
from database import db
from run import app

"""
收集单词的模块
"""


def get_word(word_txt: str) -> Word | None:
    # word先专为小写
    word_txt = word_txt.lower()
    # 数据库查找word，存在就返回
    find = Word.query.filter_by(word=word_txt).first()
    if find is not None:
        return find
    url = f'https://dict.youdao.com/jsonapi?jsonversion=2&client=mobile&q=\
    {word_txt}&dicts=%7B%22count%22%3A99%2C%22dicts%22%3A%5B%5B%22ec%22%5D%5D%7D'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            ret = response.json()
            word = Word()
            word.word = word_txt
            word.trans = ret['ec']['word'][0]['trs'][0]['tr'][0]['l']['i'][0]
            trans_index = 0
            while len(word.trans) < 3 and ret['ec']['word'][0]['trs'][trans_index] is not None:
                word.trans = ret['ec']['word'][0]['trs'][trans_index]['tr'][0]['l']['i'][0]
                trans_index += 1
            db.session.add(word)
            db.session.commit()
            return word
        except Exception or KeyError as e:
            app.logger.info('未找到翻译, word: ' + word_txt)
    else:
        app.logger.info('获取单词失败', response.status_code)
    return None


def get_word_by_openai():
    prompt = '''作为词典API，我给出单词，给我返回对应的JSON，格式如下：
    {
        "word": "world", // 单词
        "trans": "n.世界", // 词性，对应的翻译(可以是多个)
        "exps": [ // 例句，可以是多个例句
            {
                "sentence": "hello world",
                "sentence_trans": "你好世界"
            }
        ]
    }'''
    print(prompt)
    pass
