from flask import Blueprint
from flask import request
import time
import os

from unity_response import UnityResponse

FileManager = Blueprint('FileManager', __name__, url_prefix="/api/file")


@FileManager.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file:
        # 保存文件到指定路径
        # file.save('./uploads/' + file.filename)
        # 以当前时间戳+原文件名重命名文件
        try:
            file_name = str(time.time()) + '_' + file.filename
            file.save(os.path.join('./uploads/', file_name))
            return UnityResponse.success(msg='上传成功, 文件名: ' + file_name, data={
                'name': file_name
            })
        except Exception as e:
            return UnityResponse.error(msg='上传失败, ' + str(e))
    else:
        return UnityResponse.error(msg='无文件')
