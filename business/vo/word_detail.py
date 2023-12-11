from dataclasses import dataclass

from business.models import Word


@dataclass
class WordDetail:
    id: int = 0
    word: str = ''
    trans: str = ''
    tags: list = None,
    usphone: str = ''
    usspeech: str = ''
    rem_method: str = ''
    abouts: list = None
    roots: list = None
    root: str = ''
    # 下面是一些个人数据
    learned: bool = False
    error_count: int = 0
    killed: bool = False
    pitch_count: int = 0

    def __init__(self, oid: int, word: str, trans: str, usphone: str = '',
                 usspeech: str = '', rem_method: str = '', root: str = ''):
        self.id: int = oid
        self.word: str = word
        self.trans: str = trans
        self.tags: list = []
        self.usphone: str = usphone
        self.usspeech: str = usspeech
        self.rem_method: str = rem_method
        self.abouts: list = []
        self.roots: list = []
        self.root: str = root

    @classmethod
    def word_2_vo(cls, w: Word):
        ret_vo = WordDetail(w.id, w.word, w.trans_cn, w.usphone, w.usspeech, w.rem_method, w.root)

        # 个人数据
        for tag in w.type.split('|'):
            if tag == 'CET4':
                ret_vo.tags.append('CET4')
            elif tag == 'KAO_YAN':
                ret_vo.tags.append('考研')
        else:
            ret_vo.tags = [w.type]

        if ret_vo.usspeech == '':
            ret_vo.usspeech = ret_vo.word + '&type=2'

        return ret_vo
