from django.contrib import admin
from .models import User, UserAnimeFavorite


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_active', 'last_login']
    list_display_links = ['id', 'username']


@admin.register(UserAnimeFavorite)
class UserAnimeFavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'anime', 'created_at']
    list_display_links = ['id']
    list_filter = ['user', 'anime', 'created_at']
