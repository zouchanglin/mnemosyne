from dataclasses import dataclass

from business.models import Word


@dataclass
class WordVO:
    id: int = 0
    word: str = ''
    trans: str = ''
    tags: list = None

    def __init__(self, id: int, word: str, trans: str):
        self.id: int = id
        self.word: str = word
        self.trans: str = trans
        self.tags: list = []

    # builder mode

    def set_word(self, word: str):
        self.word = word
        return self

    def set_trans(self, trans: str):
        self.trans = trans
        return self

    @classmethod
    def word_2_vo(cls, w: Word):
        ret_vo = WordVO(w.id, w.word, w.trans_cn)
        for tag in w.type.split('|'):
            if tag == 'CET4':
                ret_vo.tags.append('CET4')
            elif tag == 'KAO_YAN':
                ret_vo.tags.append('考研')
        return ret_vo

    # tostring
    def __repr__(self):
        return self.word + " " + self.trans
