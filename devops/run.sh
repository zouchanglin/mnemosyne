# 先判断venv是否存在，不存在则创建
if [ ! -d "venv" ]; then
  mkdir venv
  python3 -m venv venv
  echo 'devops venv created!'
fi

echo 'devops venv activate!'
source ./venv/bin/activate

echo 'devops pip install!'
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

echo 'devops run!'
python3 workflow.py
