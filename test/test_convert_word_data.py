import json
import pytest
from app import app
from database import db
from business.models import Word


def replace_fran(line):
    """
    先处理一行中的法语字符
    :param line:
    :return:
    """
    fr_en = [['é', 'e'], ['ê', 'e'], ['è', 'e'], ['ë', 'e'], ['à', 'a'], ['â', 'a'], ['ç', 'c'], ['î', 'i'], ['ï', 'i'],
             ['ô', 'o'], ['ù', 'u'], ['û', 'u'], ['ü', 'u'], ['ÿ', 'y']
             ]
    for i in fr_en:
        line = line.replace(i[0], i[1])
    return line


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
        yield client


def test_insert_word(client):
    with app.app_context():
        is_cet4 = False
        if is_cet4:
            filename = "./origin/CET4luan_2.json"
        else:
            filename = "./origin/KaoYan_2.json"

        file = open(filename, 'r', encoding='utf-8')
        line_count = 0
        # 其实只需要ID-Word /音标/ -词性-释义 [助记] [关联词]
        for line in file.readlines():
            word = Word()
            word.type = 'CET4' if is_cet4 else 'KAO_YAN'
            word.type_line = line_count
            line = replace_fran(line.strip())
            try:
                word_json = json.loads(line)
                word.word = word_json['headWord']

                # 先查一下已有词库
                has_word = Word.query.filter_by(word=word_json['headWord']).first()
                if has_word:
                    has_word.type = 'CET4|KAO_YAN'
                    # has_word.type_line = word.type_line
                    # 更新一下
                    db.session.commit()
                    print('已有词库:', has_word)
                    continue

                content = word_json['content']['word']['content']
                trans_str = ""
                for tran in content['trans']:
                    trans_str += tran['pos'] + "." + tran['tranCn'] + "\n"
                word.trans_cn = trans_str
                if 'usphone' in content:
                    word.usphone = content['usphone']
                if 'remMethod' in content:
                    word.rem_method = content['remMethod']['val']
                if 'usspeech' in content:
                    word.usspeech = content['usspeech']
                db.session.add(word)
            except Exception as e:
                print(e, line)
            line_count += 1
        file.close()
        print("总共:" + str(line_count) + "条数据")
        db.session.commit()
