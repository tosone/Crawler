import logging
from logging.handlers import RotatingFileHandler

#################################################################################################
# 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
Rthandler = RotatingFileHandler('myapp.log', maxBytes=1000)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('').addHandler(Rthandler)

while True:
    logging.error("wrong")
