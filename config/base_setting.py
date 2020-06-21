SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8899
DEBUG = True
AUTH_COOKIE_NAME = 'food_order'

##过滤url
IGNORE_URLS = [
    '^/user/login',
    '^/api'
]

IGNORE_STATIC_URLS = [
    '^/static',
    '^/favicon.ico'
]


PAGE_SIZE = 3
PAGE_DISPLAY = 5


STATUS_MAPPING = {
    "-1":"请选择状态",
    "1":"正常",
    "0":"已删除"
}

SEX_MAPPING = {
    "0":"未知",
    "1":"男",
    "2":"女"
}

MINA_APP = {
    'appid': 'wxc799b33abd0e4f8d',
    'appkey': '816b4ef34ab27a70404dae4829047d7f'

}

MINA_URL = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code=' \
           '{}&grant_type=authorization_code'