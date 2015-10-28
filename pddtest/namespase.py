# -*- coding: utf-8 -*-
from api.namespace import MainNamespace
from pddtest.generator import generate_test
from pddtest.resource import PddTest, TestFailed, TestSuccess
import logging

logger = logging.getLogger('PDD test')

class PddTestNamespace(MainNamespace):

    class Meta:
        allowed_methods = ('on_GET', 'on_UPDATE', 'recv_connect')
        path = '/test'

    def __init__(self, environ, ns_name, request=None):
        MainNamespace.__init__(self, environ=environ, ns_name=ns_name, request=request)
        self.pdd_test = None

    def recv_connect(self):
        logger.info("Connect from %s" % self.environ)

    def recv_disconnect(self):
        logger.info("Received disconnect %s" % self.environ)
        self.disconnect()

    def on_GET(self, parts=[1, 2, 3, 4, 5, 6, 7]):
        test = generate_test(parts)
        self.pdd_test = PddTest.wrap(test, 1)
        self.emit('set', test.to_json())

    def on_UPDATE(self, question_index, variant):
        try:
            result = self.pdd_test.is_right_variant(question_index, variant)
            self.emit('update', question_index, result)
        except TestFailed:
            self.emit('finish', False)
            self.pdd_test = None
        except TestSuccess:
            self.emit('finish', True)
            self.pdd_test = None
        except Exception as err:
            self.emit('error', str(err))
