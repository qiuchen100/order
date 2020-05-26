# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request
from common.models.user import User
from common.libs.Helper import iPagination
from common.libs.UrlManager import UrlManager
from application import app

route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    page = request.args.get('p', 1)
    query = User.query
    page_size = app.config['PAGE_SIZE']
    display = app.config['PAGE_DISPLAY']
    params = {
        'page': page,
        'total': query.count(),
        'page_size': page_size,
        'display': display,
        'url': '/account/index'
    }
    pages = iPagination(params)
    offset = (page - 1) * page_size
    limit = page * page_size
    user_list = User.query.order_by(User.uid.desc()).all()[offset:limit]
    return render_template('account/index.html', user_list=user_list, pages=pages)


@route_account.route('/info')
def info():
    uid = request.args.get('uid')
    if not uid:
        return redirect(UrlManager.buildUrl('/account/index'))
    user_info = User.query.filter_by(uid=uid).first()
    if not user_info:
        return redirect(UrlManager.buildUrl('/account/index'))
    return render_template('account/info.html', user_info=user_info)


@route_account.route('/set', methods=['GET', 'POST'])
def set():
    resp = {'code': 200, 'msg': '添加新账户成功！', 'data': {}}
    if request.method == 'GET':
        uid = request.args.get('uid')
        user_info = User.query.filter_by(uid=uid).first() if uid else None
        return render_template('account/set.html', user_info=user_info)
    req = request.values
    nickname = req.get('nickname')
    mobile = req.get('mobile')
    email = req.get('email')
    login_name = req.get('login_name')
    login_pwd = req.get('login_pwd')


@route_account.route('/ops', methods=['POST'])
def ops():
    return render_template('account/set.html')
