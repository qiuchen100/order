# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, make_response, redirect, render_template
import json
from common.models.user import User
from common.libs.UserService import UserService
from application import app
from common.libs.UrlManager import UrlManager


route_user = Blueprint('user_page', __name__)


@route_user.route('/login', methods=['GET', 'POST'])
def login():
    resp = {'code' : 200, 'msg' : '登录成功！', 'data' : {}}
    if request.method == 'GET':
        return render_template('user/login.html')
    req = request.values
    login_name = req.get('login_name')
    login_pwd = req.get('login_pwd')

    if not login_name:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名！'
        return jsonify(resp)
    if not login_pwd:
        resp['code'] = -1
        resp['msg'] = '请输入正确的密码！'
        return jsonify(resp)

    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名和密码！'
        return jsonify(resp)
    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名和密码！'
        return jsonify(resp)

    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '{}#{}'. \
                        format(UserService.geneAuthCode(user_info), user_info.uid))

    return response


@route_user.route('/edit')
def edit():
    return render_template('user/edit.html')


@route_user.route('/reset-pwd')
def reset_pwd():
    return render_template('user/reset_pwd.html')


@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response