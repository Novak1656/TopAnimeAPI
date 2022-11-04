from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_kwargs):
        if not email:
            raise ValueError("You have not entered an email")
        if not username:
            raise ValueError("You have not entered an username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password):
        return self._create_user(email, username, password)

    def create_superuser(self, email, username, password):
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='Логин',
        max_length=255,
        unique=True,
        validators=[MinLengthValidator(8)]
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True
    )
    is_staff = models.BooleanField(
        verbose_name='Админ',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class UserAnimeFavorite(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    anime = models.ForeignKey(
        verbose_name='Аниме',
        to='main_app.Anime',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Избранное аниме'
        verbose_name_plural = 'Избранные аниме'
        ordering = ['user']

    def __str__(self):
        return f'{self.user} {self.anime}'
