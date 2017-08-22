#coding:utf-8

from django.http import HttpResponse
import requests
import random
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

# Create your views here.

# 百度翻译
def baidu(request):
    q = str(request.GET.get('p', False))
    to = str(request.GET.get('to', False))
    salt = str(random.randint(0, 10000000000))
    appid = '20170706000063079'

    # md5生成
    baiduMd5 = str(appid) + str(q) + str(salt) + 'oYWaEAE5yJMtWP01T0d3'
    md5 = hashlib.md5()
    md5.update(baiduMd5.encode("utf-8"))
    md = md5.hexdigest()
    text = 'http://api.fanyi.baidu.com/api/trans/vip/translate' + '?q=' + q + '&from=auto' + '&to=' + to + '&appid=' + appid + '&salt=' + salt + '&sign=' + md
    parameter = {
        'q': q,
        'from': 'auto',
        'to': to,
        'appid': appid,
        'salt': salt,
        'sign': md
    }
    center = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate', params=parameter)
    center = json.loads(center.text)
    center = json.dumps(center, ensure_ascii=False)
    return HttpResponse(center)

#有道翻译
def youdao(request):
    q = str(request.GET.get('p', False))
    to = str(request.GET.get('to', False))
    salt = str(random.randint(0, 10000000000))
    appKey = '10e20138310b5dda'

    # md5生成
    youdaoMd5 = str(appKey) + str(q) + str(salt) + 'SQq0cD6LKDzo0j94Fk3Ep3G82LDmOJ6v'
    md5 = hashlib.md5()
    md5.update(youdaoMd5.encode("utf-8"))
    md = md5.hexdigest()
    text = 'http://openapi.youdao.com/api' + '?q=' + q + '&from=auto' + '&to=auto' + '&appKey=' + appKey + '&salt=' + salt + '&sign=' + md
    parameter = {
        'q': q,
        'from': 'auto',
        'to': to,
        'appKey': appKey,
        'salt': salt,
        'sign': md
    }
    center = requests.get('http://openapi.youdao.com/api', params=parameter)
    center = json.loads(center.text)
    center = json.dumps(center, ensure_ascii=False)
    return HttpResponse(center)