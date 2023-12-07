# mnemosyne

```bash
pip install -r requirements.txt

# 国内清华源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```


```shell
gunicorn -w 4 \
  --access-logfile log/access.log  \
  --error-logfile log/error.log  \
  -p log/gunicorn.pid  \
  -b 0.0.0.0:5005 app:app 
```

4进程方式启动 gunicorn


docker build
```shell
docker build -t zouchanglin/mnemosyne:1.0 ./
```
