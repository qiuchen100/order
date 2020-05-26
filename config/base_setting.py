SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8899
DEBUG = True
AUTH_COOKIE_NAME = 'food_order'

##过滤url
IGNORE_URLS = [
    '^/user/login'
]

IGNORE_STATIC_URLS = [
    '^/static',
    '^/favicon.ico'
]


PAGE_SIZE = 50
PAGE_DISPLAY = 10