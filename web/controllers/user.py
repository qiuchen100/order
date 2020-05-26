# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, make_response, redirect, render_template, g
from common.models.user import User
from common.libs.UserService import UserService
from application import app, db
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

    response = make_response(jsonify(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '{}#{}'. \
                        format(UserService.geneAuthCode(user_info), user_info.uid))
    return response


@route_user.route('/edit', methods=['GET', 'POST'])
def edit():
    resp = {'code': 200, 'msg': '账户信息修改成功！', 'data': {}}
    if request.method == 'GET':
        return render_template('user/edit.html', current='edit')
    req = request.values
    mobile = req.get('mobile')
    nickname = req.get('nickname')
    email = req.get('email')
    if not mobile:
        resp['code'] = -1
        resp['msg'] = '请输入正确的手机号！'
        return jsonify(resp)
    if not nickname:
        resp['code'] = -1
        resp['msg'] = '请输入正确的姓名！'
        return jsonify(resp)
    if not email:
        resp['code'] = -1
        resp['msg'] = '请输入正确的邮箱！'
        return jsonify(resp)

    user_info = g.current_user
    user_info.mobile = mobile
    user_info.nickname = nickname
    user_info.email = email
    db.session.add(user_info)
    db.session.commit()

    return jsonify(resp)



@route_user.route('/reset-pwd', methods=['GET', 'POST'])
def reset_pwd():
    resp = {'code': 200, 'msg': '密码修改成功！', 'data': {}}
    if request.method == 'GET':
        return render_template('user/reset_pwd.html', current='reset-pwd')
    req = request.values
    old_password = req.get('old_password')
    new_password = req.get('new_password')
    new_password2 = req.get('new_password2')

    if UserService.genePwd(old_password, g.current_user.login_salt) != g.current_user.login_pwd:
        resp['code'] = -1
        resp['msg'] = '请输入正确的原来的密码！'
        return jsonify(resp)
    if not new_password or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = '新密码的长度至少为6位！'
        return jsonify(resp)
    if new_password == old_password:
        resp['code'] = -1
        resp['msg'] = '新密码不能和原来的密码相同！'
        return jsonify(resp)
    if new_password != new_password2:
        resp['code'] = -1
        resp['msg'] = '两次输入的密码不一致，请重新输入！'
        return jsonify(resp)

    user_info = g.current_user
    user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)
    db.session.add(user_info)
    db.session.commit()

    response = make_response(jsonify(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '{}#{}'. \
                        format(UserService.geneAuthCode(user_info), user_info.uid))
    return response


@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response