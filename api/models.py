from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

# Create your models here.
from methodism.models import Otp, Token


class CustomUserManeger(UserManager):
    def create_user(self, email, password, is_staff=False, is_superuser=False, **extra):
        user = self.model(
            email=email,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra
        )
        user.set_password(str(password))
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManeger()

    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'


class OtpToken(Otp):
    email = models.CharField(max_length=128)
    by = False


class AuthToken(Token):
    pass
