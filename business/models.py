# coding: utf-8
from dataclasses import dataclass
from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, Integer, String, Boolean

from database import db

Base = db.Model
metadata = Base.metadata


class User(Base):
    __tablename__ = 'mne_user'

    id: int = Column(Integer, primary_key=True, autoincrement=True, comment='用户唯一ID')
    username: str = Column(String(32), nullable=False, default='', comment='用户名')
    password: str = Column(String(32), nullable=False, default='', comment='密码MD5')
    email: str = Column(String(32), nullable=False, default='', comment='邮箱')
    create_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')), comment='创建时间')
    update_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')),
                                   onupdate=datetime.now(pytz.timezone('Asia/Shanghai')), comment='更新时间')


class UserProfile(Base):
    """
    用户的个人配置表
    """
    __tablename__ = 'mne_user_profile'
    user_id: int = Column(Integer, primary_key=True, autoincrement=False, default=0, comment='用户ID也是主键')
    day_learn: int = Column(Integer, nullable=False, default=30, comment='用户每日学习的新单词数量')
    create_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')), comment='创建时间')
    update_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')),
                                   onupdate=datetime.now(pytz.timezone('Asia/Shanghai')), comment='更新时间')

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


@dataclass
class Word(Base):
    __tablename__ = 'mne_word'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    word: str = Column(String(32), nullable=False, default='', comment='单词')
    usphone: str = Column(String(32), nullable=True, default='', comment='美式音标')
    usspeech: str = Column(String(32), nullable=True, default='', comment='美式发音')
    trans_cn: str = Column(String(256), nullable=False, default='', comment='中文翻译')
    rem_method: str = Column(String(256), nullable=True, default='', comment='记忆方法')
    type: str = Column(String(32), nullable=True, default='KAO_YAN', comment='单词书 CET4 CET6 KAO_YAN GRE')
    type_line: str = Column(Integer, nullable=False, default=0, comment='单词书行数')
    abouts: str = Column(String(256), nullable=True, default='', comment='关联词ID')
    roots: str = Column(String(256), nullable=True, default='', comment='同根词ID')
    root: str = Column(String(32), nullable=True, default='', comment='词根')
    create_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')), comment='创建时间')
    update_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')),
                                   onupdate=datetime.now(pytz.timezone('Asia/Shanghai')), comment='更新时间')

    # hash
    def __hash__(self):
        return hash(self.word)

    def __eq__(self, other):
        return self.word == other.word



@dataclass
class UserWord(Base):
    __tablename__ = 'mne_user_word'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    word_id: int = Column(Integer, nullable=False, default=0, comment='单词ID')
    user_id: int = Column(Integer, nullable=False, default=0, comment='用户ID')
    learned: bool = Column(Boolean, nullable=True, default=False, comment='是否学习过')
    error_count: int = Column(Integer, nullable=True, default=0, comment='错误次数')
    killed: bool = Column(Boolean, nullable=True, default=False, comment='是否已经记住')
    pitch_count: int = Column(Integer, nullable=True, default=0, comment='用于阅读理解的次数')
    create_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')))
    update_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')),
                                   onupdate=datetime.now(pytz.timezone('Asia/Shanghai')))


@dataclass
class EbbinghausData(Base):
    """
    用于记录艾宾浩斯遗忘曲线的数据
    """
    __tablename__ = 'mne_ebbinghaus_data'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(Integer, nullable=False, default=0, comment='用户ID')
    word_id: int = Column(Integer, nullable=False, default=0, comment='单词ID')
    learned: bool = Column(Boolean, nullable=True, default=False, comment='是否学习过')
    # ebh_time 是一个以时间戳为内容的字符串，以|分割作为艾宾浩斯的复习时间点, 以t/f表示是否完成了复习任务。例如:
    # 1698850000-t|1698853600-t|1698857200-f|143600-f|1698850000-t
    # 用户打开APP的时会以当前的时间戳计算距离复习一个单词还有多久，还是已经到了复习该单词的时间点
    # 如果第二天仍然存在未完成复习的单词，则会一起出现在当天的复习计划中，这会导致更新整个后续艾宾浩斯遗忘曲线的时间节点
    ebh_time: str = Column(String(256), nullable=False, default='0', comment='艾宾浩斯遗忘曲线时间，字符串自行解析')
    create_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')))
    update_time: DateTime = Column(DateTime, nullable=False,
                                   default=datetime.now(pytz.timezone('Asia/Shanghai')),
                                   onupdate=datetime.now(pytz.timezone('Asia/Shanghai')))
