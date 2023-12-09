import json
import os

import requests
from flask import Blueprint
from flask import request
import base64

from business.vo.word_vo import WordVO
from database import db
from run import app
from unity_response import UnityResponse
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

from business.models import Word
from business.utils.openai_client import client


API_KEY = os.environ.get("BAIDU_API_KEY")
SECRET_KEY = os.environ.get("BAIDU_SECRET_KEY")

OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

OCRAssistant = Blueprint('OCRAssistant', __name__, url_prefix="/api/ocr")

# Need OCR上传文件路径
OCR_PATH = './uploads/'


@OCRAssistant.route('/exec', methods=['POST'])
def exec_start_ocr():
    file_names = request.json['files']
    # 获取access token
    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    text = ""
    ret_exist_words = []
    for name in file_names:
        # 读取测试图片
        file_content = read_file(OCR_PATH + name)
        # 调用文字识别服务
        result = request_url(image_url, urlencode({'image': base64.b64encode(file_content)}))

        # 解析返回结果
        result_json = json.loads(result)
        for words_result in result_json["words_result"]:
            text = text + ',' + words_result["words"]
            word = words_result["words"]
            # 数据库查找word，存在就放在list里
            find = Word.query.filter_by(word=word).all()
            if len(find) > 0:
                ret_exist_words.append(find[0])
    exist_words = [r.word for r in ret_exist_words]
    # 去重
    exist_words = list(set(exist_words))
    ai_result = analyse_ocr(text)
    for word in ai_result:
        if word in exist_words:
            continue
        else:
            word = get_mission_new_word(word)
            print('获得新单词成功！word->', word)
            ret_exist_words.append(word)

    for w in ret_exist_words:
        print(w)
    return UnityResponse.success(data={
        'words': [WordVO.word_2_vo(r) for r in ret_exist_words],
    })


"""
    获取token
"""


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    result_str = ''
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    result_str = result_str.decode()
    result = json.loads(result_str)

    if 'access_token' in result.keys() and 'scope' in result.keys():
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


"""
    读取文件
"""


def read_file(image_path):
    try:
        with open(image_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print('read image file fail', e)
        return None


"""
    调用远程服务
"""


def request_url(url, data):
    req = Request(url, data.encode('utf-8'))
    try:
        f = urlopen(req)
        result_str = f.read().decode()
        return result_str
    except URLError as e:
        print(e)


def analyse_ocr(ocr_text: str):
    """
    分析OCR结果
    :return:
    """
    prompt = f'''帮我分析这段OCR数据，提取其中的英文单词:
    {ocr_text}
    仅仅给我返回标准JSON格式的单词数组即可，比如:["hello","word"]'''

    messages = [{"role": "system", "content": prompt}]
    completion = client.chat.completions.create(
        # model="gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=0.0,
    )

    try:
        return json.loads(completion.choices[0].message.content.strip())
    except json.JSONDecodeError as ignore:
        app.logger.info("JSON解析出错，内容是: %s", completion.choices[0].message.content.strip())
        return []


def get_mission_new_word(word_txt):
    url = f'https://dict.youdao.com/jsonapi?jsonversion=2&client=mobile&q=\
    {word_txt}&dicts=%7B%22count%22%3A99%2C%22dicts%22%3A%5B%5B%22ec%22%5D%5D%7D'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            ret = response.json()
            word = Word()
            word.word = word_txt
            word.usphone = ret['ec']['word'][0]['usphone']
            word.usspeech = ret['ec']['word'][0]['usspeech']
            word.trans_cn = ret['ec']['word'][0]['trs'][0]['tr'][0]['l']['i'][0]
            word.type = 'KAO_YAN'
            word.type_line = '10000'
            db.session.add(word)
            db.session.commit()
            print('添加新单词成功', word.word)
            return word
        except Exception as e:
            print(e)
            return None
    else:
        print('获取单词失败', response.status_code)
        return None
