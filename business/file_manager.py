from flask import Blueprint
from flask import request
import time
import os

from unity_response import UnityResponse

FileManager = Blueprint('FileManager', __name__, url_prefix="/api/file")


@FileManager.route('/upload', methods=['POST'])
def upload_file():
    file_names = []
    for name, file in request.files.items():
        # 保存文件到指定路径
        # 以当前时间戳+原文件名重命名文件
        try:
            file_name = str(time.time()) + '_' + file.filename
            file.save(os.path.join('./uploads/', file_name))
            file_names.append(file_name)
        except Exception as e:
            print('文件上传异常', e)
    return UnityResponse.success(msg='上传成功 ', data={
        'names': file_names
    })
