#coding:utf-8
from rest_framework.response import Response

import json

def returnCode(code, data):
    errorCode = {
        0: 'error',
        10000: 'Success',
        10001: '请求方式错误！',
        10002: '账号密码错误！',
        10003: '该名称已被使用！',
        10004: '注册成功！',
        10005: '用户冻结！',
    }
    info = {
        'code': code,
        'data': data,
        'msg': errorCode[code]
    }
    return info

def ResponseData(code, data):
    info = returnCode(code, data)
    return Response(info)