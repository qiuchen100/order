# -*- coding: utf-8 -*-
import base64, hashlib, random, string

class UserService:

    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        str = '{}-{}'.format(base64.encodebytes(pwd.encode('utf-8')), salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()


    @staticmethod
    def geneAuthCode(user_info):
        m = hashlib.md5()
        str = '{}-{}-{}-{}'.format(user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()


    @staticmethod
    def geneSalt( length = 16 ):
        keylist = [ random.choice( ( string.ascii_letters + string.digits ) ) for i in range( length ) ]
        return ( "".join( keylist ) )