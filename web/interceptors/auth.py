# -*- coding: utf-8 -*-
import re
from flask import request, redirect, g
from application import app
from common.models.User import User
from common.libs.UserService import UserService
from common.libs.UrlManager import UrlManager


@app.before_request
def before_request():
    ignore_urls = app.config['IGNORE_URLS']
    ignore_static_urls = app.config['IGNORE_STATIC_URLS']
    pattern = re.compile('%s' % '|'.join(ignore_static_urls))
    if pattern.match(request.path):
        return
    user_info = check_login()
    g.current_user = user_info
    pattern = re.compile('%s' % '|'.join(ignore_urls))
    if pattern.match(request.path):
        return
    if not user_info:
        return redirect(UrlManager.buildUrl('/user/login'))
    return


def check_login():
    '''
    判断用户是否登录
    '''
    cookies = request.cookies
    auth_cookie = cookies.get(app.config['AUTH_COOKIE_NAME'])
    if auth_cookie is None:
        return None
    auth_info = auth_cookie.split('#')
    if len(auth_info) != 2:
        return None
    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        return None
    if not user_info:
        return None
    if UserService.geneAuthCode(user_info) != auth_info[0]:
        return None
    return user_info
