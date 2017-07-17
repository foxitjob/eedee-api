#!/usr/bin/env python
# -*- coding: cp936 -*-
import os
import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
import platform

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#
# if not os.path.exists(os.path.join(BASE_DIR, 'util/')):
#     os.makedirs(os.path.join(BASE_DIR, 'util/'))

def isWindowsSystem():
    return 'Windows'in platform.system()

def isLinuxSystem():
    return 'Linux' in platform.system()

'''日志管理类'''

def init_logger(logger_name):
    if logger_name not in Logger.manager.loggerDict:
        logger1 = logging.getLogger(logger_name)
        # logger1.setLevel(logging.INFO)  # 设置最低级别
        logger1.setLevel(logging.DEBUG)  # 设置最低级别
        df = '%Y-%m-%d %H:%M:%S'
        format_str = '[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s'
        formatter = logging.Formatter(format_str, df)
        # handler all
        if isLinuxSystem():
            if not os.path.exists('/var/util/hlcms/'):
                os.makedirs('/var/util/hlcms/')
            handler1 = TimedRotatingFileHandler('/var/util/hlcms/all.util', when='D', interval=1, backupCount=7)
        else:
            handler1 = TimedRotatingFileHandler('C:\Users\humsg-all.util', when='D', interval=1, backupCount=7)
        handler1.setFormatter(formatter)
        handler1.setLevel(logging.DEBUG)
        logger1.addHandler(handler1)
        # handler error
        if isLinuxSystem():
            if not os.path.exists('/var/util/hlcms/'):
                os.makedirs('/var/util/hlcms/')
            handler2 = TimedRotatingFileHandler('/var/util/hlcms/error.util', when='D', interval=1, backupCount=7)
        else:
            handler2 = TimedRotatingFileHandler('C:\Users\humsg-error.util', when='D', interval=1, backupCount=7)
        handler2.setFormatter(formatter)
        handler2.setLevel(logging.ERROR)
        logger1.addHandler(handler2)
        # console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        #  设置日志打印格式
        console.setFormatter(formatter)
        #  将定义好的console日志handler添加到root logger
        logger1.addHandler(console)
    logger1 = logging.getLogger(logger_name)
    return logger1


logger = init_logger('runtime-util')

if __name__ == '__main__':
    logger.debug('test-debug')
    logger.info('test-info')
    logger.warn('test-warn')
    logger.error('test-error')
