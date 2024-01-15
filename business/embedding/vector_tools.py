from flask import Blueprint, request, g

from business.collect_word import get_word
from business.utils.openai_client import client
from run import app
from unity_response import UnityResponse
from business.models import Word

WordVector = Blueprint('WordVector', __name__, url_prefix="/api/vector")


def word_to_vector_db(word: Word):
    if word is None:
        return
    from milvus_tables import mem_word_collection
    mem_word_collection.insert(
        [
            {
                "id": word.id,
                "content": word.word + ' ' + word.trans,
                "embedded": get_embedding(word.word + ' ' + word.trans)
            }
        ]
    )


def get_embedding(word_txt: str):
    # 通过openai获取单词的向量
    # word先专为小写
    word_txt = word_txt.lower().replace("\n", " ")
    embedding = client.embeddings.create(input=[word_txt],
                                         model='text-embedding-ada-002').data[0].embedding
    return embedding


@WordVector.route('/search', methods=['POST'])
def search():
    user_id = g.user_id
    app.logger.info(f'用户 {user_id} 查询向量化查词')

    data = request.get_json()
    word_txt = data.get('word', '')
    if word_txt == '':
        return UnityResponse.error(msg='参数错误！')

    # 查词
    word = Word.query.filter_by(word=word_txt).first()
    if word is None:
        word = get_word(word_txt)
        if word is None:
            return UnityResponse.error(msg='单词获取失败')
    # embedding = get_embedding(word.word + ' ' + word.trans)

    # 直接用ID先搜向量
    from milvus_tables import mem_word_collection
    try:
        embedding = mem_word_collection.query(expr=f'id in [{word.id}]',
                                              output_fields=["embedded", "content"])[0]['embedded']
    except Exception as e:
        app.logger.exception(e)
        return UnityResponse.error(msg='请稍后再试')

    search_params = {"metric_type": "IP", "params": {"nprobe": 5}, "offset": 0}
    # 搜索
    from milvus_tables import mem_word_collection
    results = mem_word_collection.search(
        data=[embedding],
        anns_field="embedded",
        param=search_params,
        limit=10,
        expr=None,
        output_fields=['id', 'content'],
    )

    # 返回结果
    src_ids = []
    for entity in results[0]:
        # 只保留相似度大于0.8的
        if entity.distance >= 0.8 and entity.id != word.id:
            src_ids.append(entity.fields['id'])

    # 根据src_id查询数据库
    words = Word.query.filter(Word.id.in_(src_ids)).all()
    return UnityResponse.success(msg='查询成功', data=words)
