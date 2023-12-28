from flask import Blueprint, request, g
from unity_response import UnityResponse
from business.models import Word

WordVector = Blueprint('WordVector', __name__, url_prefix="/api/vector")


@WordVector.route('/search', methods=['POST'])
def search():
    user_id = g.user_id
    word_ids = request.json['word_ids']
    # 每个单词的关联词，建议传3-6
    search_limit = request.json.get('search_limit', 4)

    # 肯定是直接采用向量搜索会比较快
    use_embeddings_search = request.json.get('search_by_embeddings', True)
    final_ret = []
    return UnityResponse.success(msg='查询成功', data=final_ret)
