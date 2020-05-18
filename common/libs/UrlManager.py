# -*- coding: utf-8 -*-

import time


class UrlManager(object):

    def __init__(self):
        super().__init__()

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        version = str(time.time())
        path = '/static{}?ver={}'.format(path, version)
        return UrlManager.buildUrl(path)
