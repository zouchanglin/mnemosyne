from flask_sqlalchemy import SQLAlchemy

"""
db对象，在app.run中初始化 避免循环引用
"""
db = SQLAlchemy()

