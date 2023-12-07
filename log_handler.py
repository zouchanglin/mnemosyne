import logging


# log配置，实现日志自动按日期生成日志文件
def get_log_handler():
    # 创建一个日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # 创建一个文件处理器，将日志写入到本地文件
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)
    # 创建一个日志格式化器
    # 设置日志的格式-发生时间-日志等级-日志信息文件名-函数名-行数-日志信息
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')

    # 将格式化器添加到处理器中
    file_handler.setFormatter(formatter)

    return file_handler
