#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
import settings
monkey.patch_all(thread=False, socket=False)
from socketio import socketio_manage
from socketio.server import SocketIOServer
import mimetypes
import logging

logger = logging.getLogger('API: runserver')


class PddApplication(object):
    def __init__(self):
        self.static_path = 'static'
        self.request = {
        }

    def get_from_static(self, start_response, url):
        """
        Get files from static
        :param url: HTTP url
        :return:
        """
        log = logger.getChild("get_from_static")
        if url == '/':
            url = '/index.html'
        try:
            path = ''.join([self.static_path, url])
            with open(path, 'r') as file:
                content = file.read()
                content_type = self.get_file_content_type(path)
                headers = [('Content-Type', content_type)]
                start_response('200 OK', headers)
                return [content]
        except Exception as err:
            log.warning("Client: , url: {} error: {}".format(url, err))
            content = "<h1>Not Found</h1>"
            headers = [('Content-Type', 'text/html')]
            start_response('404 Not Found', headers)
            return [content]

    def get_file_content_type(self, filepath):
        """
        Get HTTP content type of file
        :param filepath: path to file
        :return: Content-Type
        """
        url = urllib.pathname2url(filepath)
        return mimetypes.guess_type(url)[0]

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        try:
            if path.startswith('/socket.io'):
                ws_namespaces = settings.NAMESPACES.copy()
                socketio_manage(environ, ws_namespaces, self.request)
            else:
                return self.get_from_static(start_response, path)
            return
        except:
            logger.exception("API: Server exception wrapper")


if __name__ == '__main__':
    logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(name)s > %(message)s',
                        level=logging.DEBUG,
                        )
    import urllib
    SocketIOServer((settings.SERVER_ADDRESS, settings.SERVER_PORT), PddApplication(),
                   resource="socket.io", transports=['websocket']).serve_forever()
