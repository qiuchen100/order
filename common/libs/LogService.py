# -*- coding: utf-8 -*-
from flask import request, g
import json
from common.models.AppAccessLog import AppAccessLog
from common.models.AppErrorLog import AppErrorLog
from common.libs.Helper import getCurrentDate
from application import db

class LogService:

    @staticmethod
    def addAccessLog():
        user_info = g.current_user if 'current_user' in g else None
        target = AppAccessLog()
        if user_info:
            target.uid = user_info.uid
        target.referer_url = request.referrer
        target.target_url = request.url
        target.query_params = json.dumps(request.values.to_dict())
        target.ua = request.headers.get('User-Agent')
        target.ip = request.remote_addr
        target.created_time = getCurrentDate()
        db.session.add(target)
        db.session.commit()
        return True

    @staticmethod
    def addErrorLog(content):
        if 'favicon.ico' in request.url:
            return
        target = AppErrorLog()
        target.referer_url = request.referrer
        target.target_url = request.url
        target.query_params = json.dumps(request.values.to_dict())
        target.content = content
        target.created_time = getCurrentDate()
        db.session.add(target)
        db.session.commit()
        return True