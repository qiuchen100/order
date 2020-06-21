# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, request, jsonify
from sqlalchemy import or_
from common.models.member import Member
from common.libs.Helper import iPagination, getCurrentDate
from common.libs.UrlManager import UrlManager
from application import app, db

route_member = Blueprint('member_page', __name__)


@route_member.route('/index')
def index():
    page = int(request.args.get('p', 1))
    query = Member.query
    page_size = app.config['PAGE_SIZE']
    display = app.config['PAGE_DISPLAY']

    mix_kw = request.values.get('mix_kw')
    status = request.values.get('status')

    if mix_kw:
        rule = or_(Member.nickname.ilike('%{}%'.format(mix_kw)),
                   Member.mobile.ilike('%{}%'.format(mix_kw)))
        query = query.filter(rule)
    if status and int(status) > -1:
        query = query.filter(Member.status == status)

    url_params = ''
    for arg in request.values:
        url_params += '&' + arg + "=" + request.values.get(arg)

    params = {
        'page': page,
        'total': query.count(),
        'page_size': page_size,
        'display': display,
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(params)
    offset = (page - 1) * page_size
    limit = page * page_size

    member_list = query.order_by(Member.id.desc()).all()[offset:limit]
    status_mapping = app.config['STATUS_MAPPING']
    return render_template('member/index.html', member_list=member_list, pages=pages,
                           status_mapping=status_mapping, params=request.values)


@route_member.route('/info')
def info():
    id = request.args.get('id')
    if not id:
        return redirect(UrlManager.buildUrl('/member/index'))
    member_info = Member.query.filter_by(id=id).first()
    if not member_info:
        return redirect(UrlManager.buildUrl('/member/index'))
    return render_template('member/info.html', member_info=member_info)


@route_member.route('/set', methods=['GET', 'POST'])
def set():
    resp = {'code': 200, 'msg': '修改会员账号成功！', 'data': {}}
    if request.method == 'GET':
        id = request.args.get('id')
        if not id:
            return redirect(UrlManager.buildUrl('/member/index'))
        member_info = Member.query.filter_by(id=id).first()
        if not member_info:
            return redirect(UrlManager.buildUrl('/member/index'))
        return render_template('member/set.html', member_info=member_info)
    req = request.values
    id = req.get('id', 0)
    nickname = req.get('nickname')
    if nickname is None or len( nickname ) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~~"
        return jsonify( resp )

    member_info = Member.query.filter(Member.id == id, Member.nickname == nickname).first()
    if member_info:
        resp['code'] = -1
        resp['msg'] = "用户名不可以和上一次的一样~~"
        return jsonify(resp)
    member_info = Member.query.filter(Member.id == id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "指定的会员不存在~~"
        return jsonify(resp)
    member_info.nickname = nickname
    member_info.updated_time = getCurrentDate()
    db.session.add(member_info)
    db.session.commit()
    return jsonify(resp)


@route_member.route('/ops', methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': '删除会员账户成功！', 'data': {}}
    id = request.values.get('id')
    member_info = Member.query.filter_by(id=id).first()
    if member_info:
        if member_info.status == 0:
            member_info.status = 1
            resp['msg'] = '恢复会员账户成功！'
        else:
            member_info.status = 0
            member_info.updated_time = getCurrentDate()
        db.session.add(member_info)
        db.session.commit()
        return jsonify(resp)
    resp['code'] = -1
    resp['msg'] = "会员不存在！"
    return jsonify(resp)


@route_member.route('/comment', methods=['POST'])
def comment():
    return render_template('member/comment.html')