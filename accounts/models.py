from PIL import Image
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from shortuuidfield import ShortUUIDField
from django.db import models


# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError('请传入用户名!')
        if not password:
            raise ValueError('请传入密码!')
        if not email:
            raise ValueError('请传入邮箱地址!')

        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, email, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is-staff', True)
        return self._create_user(username, password, email, **kwargs)

    def create_superuser(self, username, password, email, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)

        if kwargs.get('is_superuser') is not True:
            raise ValueError('管理员必须is_superuser=True')

        return self._create_user(username, password, email, **kwargs)


class MyUser(AbstractBaseUser, PermissionsMixin):
    GENDER_TYPE = (
        ('1', '男'),
        ('2', '女'),
        ('3', '保密'),
    )
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=128, verbose_name='用户名', unique=True,
                                help_text='不得超过128个字符，包含字母、数字，特殊字符仅@、+、-、_')
    password = models.CharField(max_length=256, verbose_name='密码',
                                help_text='')
    email = models.EmailField(verbose_name='邮箱', unique=True,
                              help_text='一个邮箱只能注册一次')
    nickname = models.CharField(max_length=20, verbose_name='昵称', null=True, blank=True)
    age = models.IntegerField(verbose_name='年龄', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', choices=GENDER_TYPE, max_length=3,
                              default='1', null=True, blank=True)
    address = models.CharField(verbose_name='地址', max_length=128, null=True, blank=True)
    identified_id = models.CharField(verbose_name='身份证', max_length=30, null=True, blank=True)
    avatar = models.ImageField(verbose_name='头像', upload_to='avatar/%Y%m%d/', null=True, blank=True)
    phone = models.CharField(verbose_name='电话', null=True, blank=True, max_length=13)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='生成日期')
    is_active = models.BooleanField(default=True, verbose_name='激活状态')
    is_staff = models.BooleanField(default=False, verbose_name='是否为员工')
    personal_profile = models.TextField(verbose_name='个人简介', max_length=500, null=True, blank=True,
                                        help_text='不得超过500字!')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['created_time']
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        user = super(MyUser, self).save(*args, **kwargs)
        if self.avatar and not kwargs.get('update_fields'):
            resize_image = change_image_size(200, self.avatar)
            resize_image.save(self.avatar.path)
        return user


def change_image_size(size, *args, **kwargs):
    image = Image.open(*args, **kwargs)
    (x, y) = image.size
    new_x = size
    new_y = int(new_x * (y / x))
    resize_image = image.resize((new_x, new_y), Image.ANTIALIAS)
    return resize_image
