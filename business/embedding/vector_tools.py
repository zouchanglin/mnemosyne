from flask import Blueprint, request, g
from chroma_db import collection
from unity_response import UnityResponse
from business.models import Word, UserWord

WordVector = Blueprint('WordVector', __name__, url_prefix="/api/vector")


@WordVector.route('/init', methods=['GET'])
def init():
    return UnityResponse.success(msg='操作成功')
    user_id = g.user_id
    current_app.logger.info('user-->{}调用向量数据库初始化!'.format(user_id))

    page_size = 500  # 每页的记录数
    # 分页查询全部的word,1页查询100条
    Word.query.paginate(page=56, per_page=100)
    query_paginate = Word.query.paginate(page=1, per_page=page_size)
    # 获取总页数
    pages = query_paginate.pages
    # 每页遍历
    for page in range(1, pages + 1):
        paginate = Word.query.paginate(page=page, per_page=page_size)
        # 每页的数据
        words = paginate.items
        vector_group_word(words)
        current_app.logger.info('成功添加1页单词, page = ', page)
    return UnityResponse.success(msg='操作成功')


@WordVector.route('/search', methods=['POST'])
def search():
    user_id = g.user_id
    word_ids = request.json['word_ids']
    # 每个单词的关联词，建议传3-6
    search_limit = request.json.get('search_limit', 4)

    # 肯定是直接采用向量搜索会比较快
    use_embeddings_search = request.json.get('search_by_embeddings', True)

    if use_embeddings_search:
        # print('使用向量搜索')
        word_ids = [str(word_id) for word_id in word_ids]
        embeddings_results = collection.get(ids=word_ids, include=["embeddings"])
        results = collection.query(query_embeddings=embeddings_results['embeddings'], n_results=search_limit)
    else:
        # 需要OpenAI向量化一次
        # 查询ID在word_ids里面的单词
        words = Word.query.filter(Word.id.in_(word_ids)).all()
        q_texts = [(word.word + " " + word.trans_cn) for word in words]
        results = collection.query(
            query_texts=q_texts,
            n_results=len(words) * search_limit,
            # 需要返回元数据
            include=["metadatas"]
        )

    final_ret = []
    for ret in results['metadatas']:
        final_ret.extend(ret)
    return UnityResponse.success(msg='查询成功', data=final_ret)


def vector_group_word(words):
    metadatas = []
    ids = [str(word.id) for word in words]
    documents = [(word.word + " " + word.trans_cn) for word in words]
    for word in words:
        metadatas.append({
            "id": word.id,
            "word": word.word,
            "trans": word.trans_cn
        })
    collection.add(
        metadatas=metadatas, documents=documents, ids=ids
    )
