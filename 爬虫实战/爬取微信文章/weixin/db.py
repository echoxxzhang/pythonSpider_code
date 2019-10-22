from redis import StrictRedis
import pickle
from request import WeixinRequest
from config import *

class RedisQueue():
    def __init__(self):
        '''
        初始化Redis
        '''
        self.db = StrictRedis(host='localhost', port=REDIS_PORT, password=REDIS_PASSWORD)

    def add(self, request):
        '''
        向队列添加序列化后的Request
        :param request: 请求对象
        :return: 添加结果
        '''
        if isinstance(request, WeixinRequest):
            return self.db.rpush(REDIS_KEY, pickle.dumps(request))
            # 判断这个请求实例是不是由WeixinRequest这个类实例化出来的
            # 如果是，将这个序列化后的对象添加在最右边
        else:
            return False

    def pop(self):
        '''
        将序列号的对象取出
        :return: Request or None
        '''
        if self.db.llen(REDIS_KEY):
            return pickle.loads(self.db.lpop(REDIS_KEY))
        else:
            return False


    def clear(self):
        self.db.delete(REDIS_KEY)

    def empty(self):
        '''
        判断列表key的长度
        :return: 布尔值
        '''
        return self.db.llen(REDIS_KEY) == 0


if __name__ == '__main__':
    db = RedisQueue()
    start_url = 'http://www.baidu.com'
    weixin_request = WeixinRequest(url=start_url, callback='hello', need_proxy=True)
    db.add(weixin_request)
    request = db.pop()
    print(request)
    print(request.callback, request.need_proxy)