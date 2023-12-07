import json
from time import sleep

import requests
from flask import Blueprint, Response, stream_with_context, current_app
from requests.exceptions import ProxyError

PingSSE = Blueprint('PingSSE', __name__, url_prefix="/api/ping")


@PingSSE.route("/sse", methods=['GET'])
def ping_open_ai():
    def check_connectivity():
        while True:
            yield 'event: ping\ndata: '
            yield check_openai_socket() + '\n'
            yield '\n'
            sleep(5)

    return Response(stream_with_context(check_connectivity()), mimetype="text/event-stream")


def check_openai_socket():
    try:
        res = requests.get('https://api.openai.com', timeout=3)
        delay = round(res.elapsed.total_seconds(), 3)
        return json.dumps({
            'connected': res.status_code == 404,
            'delay': delay if delay else 0,
            'host': 'api.openai.com',
        })
    except ProxyError as e:
        current_app.logger.info('请求 api.openai.com 超时')
        return json.dumps({
            'connected': False,
            'delay': 0,
            'host': 'api.openai.com',
        })
