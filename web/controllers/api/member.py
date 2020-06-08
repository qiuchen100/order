# -*- coding: utf-8 -*-
import requests, json
from . import route_api
from flask import jsonify, request
from application import app, db
from common.models.member import Member
from common.models.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentDate



@route_api.route("/member/login", methods=['GET', 'POST'])
def login():
    resp = {'code' : 200, 'msg' : '操作成功！', 'data' : {}}
    req = request.values
    code = req.get('code', '')
    if not code:
        resp['code'] = -1
        resp['msg'] = '需要传递code！'
        return jsonify(resp)

    url = app.config['MINA_URL']
    url = url.format(app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
    r = requests.get(url)
    res = json.loads(r.text)
    openid = res['openid']
    '''
    查询openid是否已经绑定
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = req.get('nickName', '')
        model_member.sex = req.get('gender', 0)
        model_member.avatar = req.get('avatarUrl', '')
        model_member.salt = ''
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
    resp['data'] = {'nickname': member_info.nickname}
    return jsonify(resp)