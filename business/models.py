# coding: utf-8
from dataclasses import dataclass
from typing import Union

from sqlalchemy import Column, DateTime, Integer, String, Boolean, ColumnOperators

from business.utils.common_tools import get_now_time
from database import db

Base = db.Model
metadata = Base.metadata


class User(Base):
    __tablename__ = 'mne_user'
    id: int = Column(Integer, primary_key=True, autoincrement=True, comment='用户唯一ID')
    password: str = Column(String(32), nullable=False, default='', comment='密码MD5')
    email: str = Column(String(32), nullable=False, default='', comment='邮箱')
    nickname: str = Column(String(32), nullable=False, default='', comment='用户昵称')
    create_time: DateTime = Column(DateTime, nullable=False,
                                   default=get_now_time(), comment='创建时间')
    update_time: DateTime = Column(DateTime, nullable=False,
                                   default=get_now_time(),
                                   onupdate=get_now_time(), comment='更新时间')


@dataclass
class UserProfile(Base):
    """
    用户的个人配置表
    """
    __tablename__ = 'mne_user_profile'
    user_id: int = Column(Integer, primary_key=True, autoincrement=False, default=0, comment='用户ID也是主键')
    day_learn: int = Column(Integer, nullable=False, default=30, comment='用户每日学习的新单词数量')
    create_time: DateTime = Column(DateTime, nullable=False,
                                   default=get_now_time(), comment='创建时间')
    update_time: DateTime = Column(DateTime, nullable=False,
                                   default=get_now_time(),
                                   onupdate=get_now_time(), comment='更新时间')


@dataclass
class Word(Base):
    __tablename__ = 'mne_word'
    id: Union[int, ColumnOperators] = Column(Integer, primary_key=True, autoincrement=True)
    word: str = Column(String(32), nullable=False, default='', comment='单词')
    trans: str = Column(String(256), nullable=False, default='', comment='中文翻译')
    create_time: DateTime = Column(DateTime, nullable=False,
                                   default=get_now_time(), comment='创建时间')
    update_time: DateTime = Column(DateTime, nullable=False,
                                   default=get_now_time(),
                                   onupdate=get_now_time(), comment='更新时间')

    # hash
    def __hash__(self):
        return hash(self.word)

    def __eq__(self, other):
        return self.word == other.word


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
                                   default=get_now_time())
    update_time: DateTime = Column(DateTime, nullable=False,
                                   default=get_now_time(),
                                   onupdate=get_now_time())
