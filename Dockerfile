#使用的基础镜像
#FROM python:3.9.0

FROM python:3.11.7-slim-bullseye

#设置工作目录
WORKDIR /app
#复制requirements.txt
COPY requirements.txt requirements.txt
#安装依赖包
RUN pip install pysqlite3-binary
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
#复制当前目录下的内容到docker中
COPY . .
EXPOSE 5005

RUN mkdir ./log

CMD ["python", "app.py"]

#启动命令
#CMD ["gunicorn", "-w", "4",\
#        "--access-logfile", "log/access.log",\
#        "--error-logfile", "log/error.log",\
#        "-p", "log/gunicorn.pid",\
#        "-b", "0.0.0.0:5005", "app:app"]

