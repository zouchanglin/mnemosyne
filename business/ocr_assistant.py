import json
import os

from flask import Blueprint
from flask import request
import base64

from business.collect_word import get_word
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
    ret_words: list[Word] = []
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
            # word先专为小写
            word = word.lower()
            # 数据库查找word，存在就放在list里
            ret_words.append(get_word(word))
    # 对ret_words进行去重
    ret_words = list(set(ret_words))
    # 去掉null元素
    ret_words = list(filter(lambda x: x is not None, ret_words))
    return UnityResponse.success(data={
        'words': ret_words,
    })


def fetch_token():
    """
    获取token
    """
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


def read_file(image_path):
    """
    读取文件
    """
    try:
        with open(image_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print('read image file fail', e)
        return None


def request_url(url, data):
    """
    调用远程服务
    """
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
    ocr_text = ocr_text.lower()
    prompt = f'''帮我分析这段OCR数据，提取其中的英文单词:
    {ocr_text}
    仅仅给我返回标准JSON格式的单词数组即可，比如:["hello","word"]'''

    messages = [{"role": "system", "content": prompt}]
    completion = client.chat.completions.create(
        # https://platform.openai.com/docs/guides/text-generation/json-mode 详细说明
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=0.0,
        response_format={"type": "json_object"},
    )

    try:
        return json.loads(completion.choices[0].message.content.strip())
    except json.JSONDecodeError as ignore:
        app.logger.info("JSON解析出错，内容是: %s", completion.choices[0].message.content.strip())
        return []
