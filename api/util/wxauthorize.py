#!/usr/bin/env python
# -*- coding: cp936 -*-
from api.util.logger_helper import logger
import hashlib
import tornado.web

class WxSignatureHandler(tornado.web.RequestHandler):
    """
    ΢�ŷ�����ǩ����֤, ��Ϣ�ظ�

    check_signature: У��signature�Ƿ���ȷ
    """

    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            logger.debug('΢��signУ��,signature='+signature+',&timestamp='+timestamp+'&nonce='+nonce+'&echostr='+echostr)
            result = self.check_signature(signature, timestamp, nonce)
            if result:
                logger.debug('΢��signУ��,����echostr='+echostr)
                self.write(echostr)
            else:
                logger.error('΢��signУ��,---У��ʧ��')
        except Exception as e:
            logger.error('΢��signУ��,---Exception' + str(e))


    def check_signature(self, signature, timestamp, nonce):
        """У��token�Ƿ���ȷ"""
        token = 'test12345'
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest()
        logger.debug('sha1=' + sha1 + '&signature=' + signature)
        return sha1 == signature