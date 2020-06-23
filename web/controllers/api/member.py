# -*- coding: utf-8 -*-
import requests, json
from . import route_api
from flask import jsonify, request
from application import app, db
from common.models.Member import Member
from common.models.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentDate
from common.libs.MemberService import MemberService


@route_api.route("/member/login", methods=['GET', 'POST'])
def login():
    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values
    code = req.get('code', '')
    if not code:
        resp['code'] = -1
        resp['msg'] = '需要传递code！'
        return jsonify(resp)

    openid = MemberService.getWechatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = '调用微信openid出错！'
        return jsonify(resp)

    '''
    查询openid是否已经绑定
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = req.get('nickName', '')
        model_member.sex = req.get('gender', 0)
        model_member.avatar = req.get('avatarUrl', '')
        model_member.salt = MemberService.geneSalt()
        model_member.created_time = model_member.updated_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()
        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.created_time = model_bind.updated_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()
        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = '{}#{}'.format(MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)


@route_api.route("/member/check-reg", methods=['GET', 'POST'])
def check_reg():
    resp = {'code': 200, 'msg': '操作成功！', 'data': {}}
    req = request.values
    code = req.get('code', '')
    if not code:
        resp['code'] = -1
        resp['msg'] = '需要传递code！'
        return jsonify(resp)

    openid = MemberService.getWechatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = '调用微信openid出错！'
        return jsonify(resp)

    '''
        查询openid是否已经绑定
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = '未绑定！'
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = '未查询到绑定信息！'
        return jsonify(resp)
    token = '{}#{}'.format(MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)
