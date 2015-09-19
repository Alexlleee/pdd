# -*- coding: utf-8 -*-
from api.namespace import MainNamespace
import logging

logger = logging.getLogger('PDD test')

class PddTestNamespace(MainNamespace):

    class Meta:
        allowed_methods = ('on_GET', 'on_UPDATE', 'recv_connect')
        path = '/test'

    def recv_connect(self):
        logger.info("Connect from %s" % self.environ)

    def recv_disconnect(self):
        logger.info("Received disconnect %s" % self.environ)
        self.disconnect()

    def on_GET(self):
        data = [
            {
                'Что такое дорожное проишествие?':[
                    'Первый вариант ответа',
                    'Второй вариант ответа',
                    'Третий вариант'
                ]
            }
        ]
        self.emit('set', data)

    def on_UPDATE(self, arg):
        logger.info('User has chosen %s' % arg)
        result = {1: True}
        self.emit('update', result)
        self.emit('finish', result)
