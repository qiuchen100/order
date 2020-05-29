# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request, jsonify
from common.models.user import User
from common.libs.Helper import iPagination, getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.UserService import UserService
from application import app, db

route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    page = int(request.args.get('p', 1))
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
    default_pwd = '******'
    resp = {'code': 200, 'msg': '修改账户成功！', 'data': {}}
    if request.method == 'GET':
        uid = request.args.get('uid')
        user_info = User.query.filter_by(uid=uid).first() if uid else None
        default_pwd = default_pwd if uid else ''
        return render_template('account/set.html', user_info=user_info, default_pwd=default_pwd)
    req = request.values
    uid = req.get('uid', 0)
    nickname = req.get('nickname')
    mobile = req.get('mobile')
    email = req.get('email')
    login_name = req.get('login_name')
    login_pwd = req.get('login_pwd')

    if nickname is None or len( nickname ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify( resp )

    if mobile is None or len( mobile ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码~~"
        return jsonify( resp )

    if email is None or len( email ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱~~"
        return jsonify( resp )

    if login_name is None or len( login_name ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录用户名~~"
        return jsonify( resp )

    if login_pwd is None or len( login_pwd ) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录密码~~"
        return jsonify( resp )

    user_info = User.query.filter(User.uid!=uid, User.login_name==login_name).first()
    if user_info:
        resp['code'] = -1
        resp['msg'] = "该登录名已存在，请换一个试试~~"
        return jsonify(resp)

    model_user = User.query.filter_by(uid=uid).first() or User()
    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    model_user.nickname = nickname
    model_user.updated_time = getCurrentDate()
    if not uid:
        model_user.created_time = getCurrentDate()
        resp['msg'] = '添加新账户成功！'
    if login_pwd != '******':
        model_user.login_salt = UserService.geneSalt()
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)

    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)


@route_account.route('/ops', methods=['POST'])
def ops():
    return render_template('account/set.html')
