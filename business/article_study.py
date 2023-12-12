import threading
from queue import Queue

from flask import Blueprint, g, Response, stream_with_context

from business.services.ebbinghaus_service import get_now_need_revise_words
from business.utils.openai_client import client as ai_client
from business.models import Word

ArticleCore = Blueprint('ArticleCore', __name__, url_prefix="/api/article")


@ArticleCore.route('/generate', methods=['GET', 'POST'])
def generate():
    """
    根据今日学习的单词生成短文
    :return:
    """
    # 从全局变量获取
    user_id = g.user_id
    # 获取今天学习的单词
    word_ids = get_now_need_revise_words(user_id, strict_mode=False)
    # 获取单词
    words = Word.query.filter(Word.id.in_(word_ids)).all()
    words = [w.word for w in words]
    # words转为JSON数组字符串
    words = str(words)
    prompt = f'''给你一些单词你通过这些单词生成一篇长度100词内小短文，文章尽量短小，文章中其他单词尽量使用我提供的可选词
单词如下：
{words}
可选词:

'''
    print('prompts->', prompt)
    messages = [{"role": "system", "content": prompt}]

    def start_generate():
        stream = ai_client.chat.completions.create(
            # model="gpt-4-1106-preview",
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0.3,
            stream=True,
            max_tokens=150
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                ch = chunk.choices[0].delta.content
                print(ch, end="")
                data_queue.put(Msg('ch', ch))
        data_queue.put(Msg('base', 'over'))

    # 创建一个全局队列
    data_queue = Queue()

    def put_char():
        while True:
            item = data_queue.get(block=True)  # 阻塞等待队列
            if item is None:
                break
            yield f'event: {item.event}\ndata: {item.data}\n\n'

    threading.Thread(target=start_generate).start()
    return Response(stream_with_context(put_char()), mimetype="text/event-stream", content_type='text/event-stream')


class Msg:
    def __init__(self, event, data):
        self.event = event
        self.data = data
