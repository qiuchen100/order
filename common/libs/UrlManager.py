# -*- coding: utf-8 -*-

import time
from application import app


class UrlManager(object):

    def __init__(self):
        super().__init__()

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        release_version = app.config.get('RELEASE_VERSION')
        version = release_version if release_version else str(time.time())
        path = '/static{}?ver={}'.format(path, version)
        return UrlManager.buildUrl(path)
