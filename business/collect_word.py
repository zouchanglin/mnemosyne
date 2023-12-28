import requests

from business.models import Word
from database import db

"""
收集单词的模块
"""


def get_word(word_txt: str) -> Word:
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
            try:
                trans_index = 0
                while len(word.trans) < 3 and ret['ec']['word'][0]['trs'][trans_index] is not None:
                    word.trans = ret['ec']['word'][0]['trs'][trans_index]['tr'][0]['l']['i'][0]
                    trans_index += 1
            except Exception as e:
                word.trans = '未找到翻译'
                print(e)
            db.session.add(word)
            db.session.commit()
            return word
        except Exception as e:
            print(e)
    else:
        print('获取单词失败', response.status_code)
