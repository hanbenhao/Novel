#coding:utf-8
# 数据库导入
from web import models as web_models
from django.contrib.auth.models import User
# 框架导入
from django.http import HttpResponse, JsonResponse
from web import serializers
from rest_framework.views import APIView
# token配置导入
from rest_framework.permissions import AllowAny
from web.permissions import IsOwnerOrReadOnly
# 自定义封装函数引入
from web.config.config import ObtainIp
from web.config.errorCode import ResponseData
# 系统库引入
import time

localTime = int(time.time() * 1000)

"""
addUser添加用户
接收三个参数：
    userName：用户姓名。具有唯一性。
    password：账号密码。
    email：   邮箱
User关联表userInfo
    userID关联键值
    emailStater邮箱状态是否激活
    userStater判断用户是否被拉黑，False为未拉黑，True为拉黑
    ip用户注册ip地址
"""
class addUser(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        data = request.POST
        if data.__contains__('userName') and data.__contains__('password') and data.__contains__('email'):
            if User.objects.filter(username=data['userName']).exists(): return ResponseData(10003, False)
            # 查询user表存储数据
            User.objects.create_user(username = data['userName'], password = data['password'], email = data['email'], is_active=False)
            userInfo = User.objects.filter(username=data['userName'])
            # user关联表userInfo表，储存用户更多数据，关联字段userID，值为user表ID值，进行关联
            info = userInfo.values()
            web_models.userInfo(userID=info[0]['id'], ip=ObtainIp(request)).save()
            userInfoMore = web_models.userInfo.objects.filter(userID=info[0]['id'])
            # JSON数据格式
            userInfo = serializers.UserSerializer(userInfo, many=True).data[0]
            userInfoMore = serializers.userInfoSerializer(userInfoMore, many=True).data[0]

            userInfo['userInfoMore'] = userInfoMore
            return ResponseData(10000, userInfo)
        return ResponseData(0, False)

"""
addAdmin添加用户
接收三个参数：
    userName：用户姓名。具有唯一性。
    password：账号密码。
    email：   邮箱
"""
class addAdmin(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        data = request.POST
        if data.__contains__('userName') and data.__contains__('password') and data.__contains__('email'):
            if User.objects.filter(username=data['userName']).exists(): return ResponseData(10003, False)
            # 查询user表存储数据
            User.objects.create_user(username = data['userName'], password = data['password'], email = data['email'], is_active=True)
            userInfo = User.objects.filter(username=data['userName'])
            # user关联表userInfo表，储存用户更多数据，关联字段userID，值为user表ID值，进行关联
            info = userInfo.values()
            web_models.userInfo(userID=info[0]['id'], ip=ObtainIp(request)).save()
            userInfoMore = web_models.userInfo.objects.filter(userID=info[0]['id'])
            # JSON数据格式
            userInfo = serializers.UserSerializer(userInfo, many=True).data[0]
            userInfoMore = serializers.userInfoSerializer(userInfoMore, many=True).data[0]

            userInfo['userInfoMore'] = userInfoMore
            return ResponseData(10000, userInfo)
        return ResponseData(0, False)

"""
获取所有用户列表
接收两个参数：
    length：获取单页页面条数。
    page：  获取第几页的内容。
    length和page两个参数不存在则传递所有用户信息。
"""
class allUser(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        data = request.POST
        userAll = User.objects.all()
        num = len(userAll)
        if not data.__contains__('length') or not data.__contains__('page'):
            modelsData = serializers.UserSerializer(userAll, many=True).data
            data = {
                'data': modelsData,
                'num': num
            }
            return ResponseData(10000, data)
        else:
            length = int(data['length'])
            page = int(data['page'])
            userAll = userAll[(page - 1) * length : page * length]
            modelsData = serializers.UserSerializer(userAll, many=True).data
            data = {
                'data': modelsData,
                'num': num
            }
            return ResponseData(10000, data)

"""
用户登陆 loginUser
接收两个参数：
    userName：用户姓名。
    password：账号密码。
"""
class loginUser(APIView):
    def post(self, request, format=None):
        data = request.POST
        if data.__contains__('userName') and data.__contains__('password'):
            userInfo = web_models.user.objects.filter(userName=data['userName']).values()
            if data['password'] == userInfo[0]['password']:
                if userInfo[0]['userStater'] == False: return ResponseData(10000, False)
                return ResponseData(10005, False)
        return ResponseData(10002, False)

"""
    查询当前用户信息
    接收一个参数：
        id： User表唯一标识
"""
class UserInfo(APIView):
    def post(self, request, format=None):
        userId = request.user.id
        userInfo = User.objects.filter(id=userId)
        userInfo = serializers.UserSerializer(userInfo, many=True).data
        return ResponseData(10000, userInfo)


