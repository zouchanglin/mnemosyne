import configparser
import os

from flask import Flask
from flask import request
import subprocess

config = configparser.ConfigParser()
# 判断配置文件是否存在
if not os.path.exists('workflow.ini'):
    config['DEFAULT'] = {
        'image_tag': '1.0.0',
        'running_container_id': ''
    }
    with open('workflow.ini', 'w') as config_file:
        config.write(config_file)
        print('配置文件创建成功')
else:
    config.read('workflow.ini')
    print('配置文件读取成功')

app = Flask(__name__)

# 定义一些目录常量
DOCKER_BUILD_PATH = '/mnt/ssd/devops'
# DOCKER_BUILD_PATH = '/Users/meng/Downloads/devops'
repo_dir = DOCKER_BUILD_PATH + '/mnemosyne'
print(repo_dir)

repo_url = "git@github.com:zouchanglin/mnemosyne.git"


@app.route('/')
def index():
    return "devops for mnemosyne!"


# 1.0.0 -> 1.0.1、1.0.9 -> 1.1.0、1.9.9 -> 2.0.0
def get_new_tag(now_image_tag):
    tag_list = now_image_tag.split('.')
    if len(tag_list) != 3:
        return now_image_tag
    tag_list = [int(i) for i in tag_list]
    tag_list[2] += 1
    if tag_list[2] == 10:
        tag_list[2] = 0
        tag_list[1] += 1
    if tag_list[1] == 10:
        tag_list[1] = 0
        tag_list[0] += 1
    return '.'.join([str(i) for i in tag_list])


@app.route('/build', methods=['POST', 'GET'])
def build():
    # print(request.json)

    print('Git提交信息:', request.json['commits'][0]['message'])

    print("git push: trigger start build")
    # 1、git pull
    if not os.path.exists(repo_dir):
        # 目录不存在，使用git clone
        subprocess.run(["git", "clone", repo_url, repo_dir])
    subprocess.run(["git", "checkout", "main"], cwd=repo_dir)
    subprocess.run(["pwd"], cwd=repo_dir)
    # 目录存在，使用git pull
    subprocess.run(["git", "pull"], cwd=repo_dir)

    print("git pull: finish!")
    # 2、docker build
    print('开始构建镜像!')
    now_image_tag = config['DEFAULT']['image_tag']
    # 1.0.0 -> 1.0.1、1.0.9 -> 1.1.0、1.9.9 -> 2.0.0
    new_image_tag = get_new_tag(now_image_tag)
    subprocess.run(["docker", "build", "-t", f'mnemosyne:{new_image_tag}', "."], cwd=repo_dir)
    config['DEFAULT']['image_tag'] = new_image_tag
    with open('workflow.ini', 'w') as config_f:
        config.write(config_f)

    # 3、stop old docker
    print('停止旧容器!')
    old_container_id = config['DEFAULT']['running_container_id']
    if old_container_id != '':
        subprocess.run(["docker", "stop", old_container_id])
        subprocess.run(["docker", "rm", old_container_id])

    # 4、run new docker
    print('docker-compose启动新容器!')
    # 把tag与环境变量写入docker-compose.yaml
    with open('./docker-compose.yaml.temp', 'r') as f:
        content = f.read()
        content = content.replace('tag', new_image_tag)
        content = content.replace('openai_api_key', os.environ.get('OPENAI_API_KEY', ''))
        content = content.replace('mysql_url', os.environ.get('MYSQL_URL', ''))
        with open('./docker-compose.yaml', 'w') as wf:
            wf.write(content)
            print('docker-compose.yaml写入成功， 开始启动容器')

    subprocess.run(["docker-compose", "up", "-d"], cwd='./')

    return 'ok'


# 拉取gitpull
def pull_code(comm=''):
    os.system('cd %s && git pull %s' % (repo_dir, comm))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
