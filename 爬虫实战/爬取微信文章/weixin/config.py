REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_KEY = 'weixin'

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DATABASE = 'weixin'


PROXY_POOL_URL = 'http://localhost:5010/get'
KEYWORD = '风景'
the_dict = {
    'query': KEYWORD,
    'type': 2,
}

MAX_FAILED_TIME = 10
VALID_STATUSES = [200]
TIMEOUT = 10