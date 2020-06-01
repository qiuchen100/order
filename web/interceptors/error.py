# -*- coding: utf-8 -*-
from flask import render_template
from application import app
from common.libs.LogService import LogService

@app.errorhandler(404)
def error_404(e):
    LogService.addErrorLog(e)
    resp = {'status': 404, 'msg': '很抱歉！您访问的页面不存在'}
    return render_template('error/error.html', resp)
