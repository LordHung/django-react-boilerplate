import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from src.settings.common import MEDIA_ROOT


class UserManager(BaseUserManager):
    '''
    Dùng để tạo user vì đã custom lại user gốc của django
    '''
    def create_user(self, email, password, full_name=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Email không được để trống!')
        if not password:
            raise ValueError('Password không đuợc để trống!')
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(make_password(password))
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password, full_name=None):
        user = self.create_user(email, password, full_name=full_name, is_staff=True)
        return user

    def create_superuser(self, email, password, full_name=None):
        user = self.create_user(email, password, full_name=full_name, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, default='')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # super user
    timestamp = models.DateTimeField(auto_now_add=True)

    # Username and password field is required by default
    USERNAME_FIELD = 'email'  # make email become username
    REQUIRED_FIELD = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        else:
            return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        db_table = 'user'
