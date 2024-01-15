import sys
from typing import Union

from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

from run import app

if sys.platform.startswith('linux'):
    connections.connect("default", host="192.168.31.175", port="19530")
else:
    connections.connect("default", host="192.168.31.175", port="19530")


def init_milvus():
    """
    初始化全部的milvus表
    """
    create_word_collection()
    _load_collection_data()


mem_word_collection: Union[Collection, None]


def _load_collection_data():
    """
    加载全部的milvus表
    """
    global mem_word_collection
    mem_word_collection = Collection("mem_word")
    mem_word_collection.load()
    # mem_word_collection.query(expr="id in [1]")


def create_word_collection():
    name = "mem_word"
    # 检测集合是否存在
    if not utility.has_collection(name):
        # 定义Collection中的各个字段
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
            FieldSchema(name="embedded", dtype=DataType.FLOAT_VECTOR, dim=1536),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=4096),
        ]
        # 创建Collection
        schema = CollectionSchema(fields, "单词释义向量表")
        coll = Collection(name, schema)
        app.logger.info(f'mem_word collection created！{coll.schema}')

        # 创建完成后开始构建索引
        collection = Collection(name)

        index_params = {
            "index_type": "IVF_FLAT",
            # "metric_type": "L2", IP在语义层面应该是更加OK的
            "metric_type": "IP",
            "params": {
                "nlist": 1024
            }
        }

        collection.create_index(
            field_name="embedded",
            index_params=index_params,
            index_name="word_index"
        )
        utility.index_building_progress(name)
        app.logger.info('word_index build success!')
    else:
        app.logger.info('mem_word collection already exists')
