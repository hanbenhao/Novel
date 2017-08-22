from django.conf.urls import url
from web.views import user
from web.views import fanyi
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^apitoken$', views.obtain_auth_token),

    url(r'^baidu$', fanyi.baidu),
    url(r'^youdao$', fanyi.youdao),

    url(r'^user/addUser$', user.addUser.as_view()),
    url(r'^user/loginUser$', user.loginUser.as_view()),
    url(r'^user/allUser$', user.allUser.as_view()),
    url(r'^user/addAdmin$', user.addAdmin.as_view()),
    url(r'^user/UserInfo$', user.UserInfo.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)