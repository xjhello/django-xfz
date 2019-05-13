from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models


class UserManager(BaseUserManager):  # 从写UserManager而不是Object，Object其实就是UserManager类型的
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError('请传入手机号码！')
        if not username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码！')

        user = self.model(telephone=telephone, username=username, **kwargs)  # model就是User
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):  # 创建普通用户
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):  # 创建超级用户
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True  # 设置为管理员
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):  # 继承AbstractBaseUser，password，last_login，is_active = True已经定义好了
    # PermissionsMixin是处理权限的类
    # 我们不使用默认的自增长的主键
    # 使用uuid/用到django_shortuuid插件
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'telephone'  # 修改了唯一验证字段(默认为username)
    # telephone，username，password
    REQUIRED_FIELDS = ['username']  # 创建超级用户要求填入的字段
    EMAIL_FIELD = 'email'

    objects = UserManager()  # 从写objects方法实现自定创建用户时所要必填的字段

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
