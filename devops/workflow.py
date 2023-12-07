import os

from flask import Flask
from flask import request
import subprocess

app = Flask(__name__)

# 定义一些目录常量
DOCKER_BUILD_PATH = '/mnt/ssd/devops'
repo_dir = DOCKER_BUILD_PATH + '/mnemosyne'
print(repo_dir)

repo_url = "git@github.com:zouchanglin/mnemosyne.git"


@app.route('/')
def index():
    return "devops for mnemosyne!"


@app.route('/build', methods=['POST'])
def build():
    # print(request.json)

    print('Git提交信息:', request.json['commits'][0]['message'])

    print("git push: trigger start build")
    # 1、git pull
    if not os.path.exists(repo_dir):
        # 目录不存在，使用git clone
        subprocess.run(["git", "clone", repo_url, repo_dir])
    else:
        # 目录存在，使用git pull
        subprocess.run(["git", "pull"], cwd=repo_dir)

    print("git pull: finish!")
    # 2、docker build
    print('开始构建镜像!')
    subprocess.run(["docker", "build", "-t", "mnemosyne:latest", "."], cwd=repo_dir)

    # 3、docker run
    return 'ok'


# 拉取gitpull
def pull_code(comm=''):
    os.system('cd %s && git pull %s' % (repo_dir, comm))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
