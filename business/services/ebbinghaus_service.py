"""
艾宾浩斯遗忘曲线服务
"""
from business.models import EbbinghausData
from business.utils.common_tools import (
    get_now_timestamp,
    get_today_end_timestamp,
    get_n_days_end_timestamp,
    timestamp_2_datetime,
)
from database import db


def get_now_need_revise_words(user_id: int, strict_mode: bool = False):
    """
    获得此刻需要学习的单词
    :param user_id:
    :param strict_mode: 严格模式: 只返回从此刻之前需要复习的单词
    """
    if strict_mode:
        now_timestamp = get_now_timestamp()
    else:
        # 一整天的单词都包括
        now_timestamp = get_today_end_timestamp()

    ebh_datas = EbbinghausData.query.filter_by(user_id=user_id).all()
    ret_words = []
    for ebh_data in ebh_datas:
        if not ebh_data.learned or ebh_data.ebh_time == '':
            # 标记为未学过的单词
            continue
        ebh_time = ebh_data.ebh_time
        ebh_time_list = ebh_time.split('|')
        for ebh_time_item in ebh_time_list:
            time, learned = ebh_time_item.split('-')
            if int(time) <= now_timestamp and learned == 'f':
                # 需要复习的单词
                ret_words.append(ebh_data.word_id)
                # 这里不要break，因为可能有单词需要复习多次/遗漏过的
                # break
    return ret_words


def get_count_data(user_id: int):
    """
    获得艾宾浩斯遗忘曲线的统计数据, 5天后，每天需要复习的单词
    :param user_id:
    :return: 0天前-4天后，每天需要复习的单词
    """
    ebh_datas = EbbinghausData.query.filter_by(user_id=user_id).all()
    rets = []
    for n in range(0, 5):
        ts = get_n_days_end_timestamp(n)
        ret = 0
        for ebh_data in ebh_datas:
            if not ebh_data.learned or ebh_data.ebh_time == '':
                # 标记为未学过的单词
                continue
            ebh_time = ebh_data.ebh_time
            ebh_time_list = ebh_time.split('|')
            for ebh_time_item in ebh_time_list:
                time, learned = ebh_time_item.split('-')
                if int(time) <= ts and learned == 'f':
                    # 需要复习的单词
                    # ret_words.append(ebh_data.word_id)
                    ret += 1
                    break
        rets.append(ret)
    # 返回的是未来5天的复习量
    return rets


def learned_or_forget_word_once(word_id: int, user_id: int, action: bool):
    """
    标记对一个单词学过/忘记一次，将影响艾宾浩斯遗忘曲线
    :param word_id:
    :param user_id:
    :param action: 进一步/退一步
    :return:
    """
    ebh_data = EbbinghausData.query.filter_by(user_id=user_id, word_id=word_id).first()
    if ebh_data is None:
        ebh_data = EbbinghausData()
        ebh_data.user_id = user_id
        ebh_data.word_id = word_id
        # 生成艾宾浩斯遗忘数据
        ebh_data.ebh_time = _calc_ebbinghaus_next_time('')
    else:
        # 更新艾宾浩斯遗忘数据
        if action:
            ebh_data.ebh_time = _calc_ebbinghaus_next_time(ebh_data.ebh_time)
        else:
            ebh_data.ebh_time = _calc_ebbinghaus_back_time(ebh_data.ebh_time)
    ebh_data.learned = action
    db.session.add(ebh_data)
    db.session.commit()


def set_word_no_learned(word_id: int, user_id: int):
    """
    标记一个单词为未学习
    :param word_id:
    :param user_id:
    :return:
    """
    ebh_data = EbbinghausData.query.filter_by(user_id=user_id, word_id=word_id).first()
    if ebh_data is not None:
        ebh_data.learned = False
        ebh_data.ebh_time = ''
        db.session.add(ebh_data)
        db.session.commit()


def _calc_ebbinghaus_next_time(time_str: str):
    """
    艾宾浩斯进一步
    :param time_str:
    :return:
    """
    if time_str == '':
        timestamp = get_now_timestamp()
        # 生成遗忘数据
        return _gen_ebbinghaus_time(timestamp)
    else:
        # 解析旧的数据 (其实只需要替换最近的一个未学为已学即可)
        return time_str.replace('f', 't', 1)


def _calc_ebbinghaus_back_time(time_str: str):
    """
    艾宾浩斯退一步
    :param time_str:
    :return:
    """
    if time_str == '':
        return ''
    else:
        # 解析旧的数据 (其实只需要替换最后的一个已学为未学即可)
        return time_str[::-1].replace('t', 'f', 1)[::-1]


def _gen_ebbinghaus_time(start_timestamp: int):
    # now-30分钟-1小时-3小时-10小时-1天-2天-6天-14天-1个月-2个月-6个月
    time_gaps = [
        0,
        1800,
        3600 * 1,
        3600 * 3,
        3600 * 10,
        3600 * 24,
        3600 * 24 * 2,
        3600 * 24 * 6,
        3600 * 24 * 14,
        3600 * 24 * 30,
        3600 * 24 * 60,
        3600 * 24 * 180,
    ]

    ret_time = ""
    for i in range(len(time_gaps)):
        ret_time += str(start_timestamp + time_gaps[i])
        if i == 0:
            ret_time += "-t"
        else:
            ret_time += "-f"
        if i != len(time_gaps) - 1:
            ret_time += "|"
    return ret_time


def test_calc_ebbinghaus_time():
    print("\n")
    print(_calc_ebbinghaus_next_time('1698854063-t|1698855863-t|1698857663-f|1698864863-f|1698890063-f|1698940463-f'
                                     '|1699026863-f|1699372463-f|1700063663-f|1701446063-f|1704038063-f|1714406063-f'))
    # 1698854063-t|1698855863-t|1698857663-t|1698864863-f|1698890063-f|1698940463-f|1699026863-f|1699372463-f|1700063663-f|1701446063-f|1704038063-f|1714406063-f
    print("\n")
    print(_calc_ebbinghaus_back_time('1698854063-t|1698855863-t|1698857663-t|1698864863-f|1698890063-f|1698940463-f'
                                     '|1699026863-f|1699372463-f|1700063663-f|1701446063-f|1704038063-f|1714406063-f'))
