# -*- coding: utf-8 -*-
import base64, hashlib, random, string
import requests, json
from application import app


class MemberService:
    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        str = '{}-{}'.format(base64.encodebytes(pwd.encode('utf-8')), salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()


    @staticmethod
    def geneSalt( length = 16 ):
        keylist = [ random.choice( ( string.ascii_letters + string.digits ) ) for i in range( length ) ]
        return ("".join(keylist))

    @staticmethod
    def geneAuthCode(member_info):
        m = hashlib.md5()
        str = '{}-{}-{}'.format(member_info.id, member_info.salt, member_info.status)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def getWechatOpenId(code):
        url = app.config['MINA_URL']
        url = url.format(app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = res.get('openid')
        return openid

