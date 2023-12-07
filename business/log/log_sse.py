from flask import Blueprint, Response, stream_with_context, current_app


LogSSE = Blueprint('LogSSE', __name__, url_prefix="/api/log")


@LogSSE.route("/sse", methods=['GET'])
def log_read():
    def print_logs():
        with open('app.log') as f:
            while True:
                # 只读最新的100行
                lines = f.readlines()[-100:]
                for line in lines:
                    if not line:
                        # 文件末尾，等待新的数据写入
                        continue
                    yield 'event: message\ndata: '
                    yield line
                    yield '\n'

    return Response(stream_with_context(print_logs()), mimetype="text/event-stream")
