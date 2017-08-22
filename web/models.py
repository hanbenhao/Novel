from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


"""
userID关联键值
    emailStater邮箱状态是否激活
    userStater判断用户是否被拉黑，False为未拉黑，True为拉黑
    ip用户注册ip地址
"""
class userInfo(models.Model):
    userID = models.CharField(max_length=30)
    emailStater = models.BooleanField(default=False)
    userStater = models.BooleanField(default=False)
    ip = models.CharField(max_length=30)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)