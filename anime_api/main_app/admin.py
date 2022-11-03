from django.contrib import admin
from .models import Anime, Genre, Studio

admin.site.site_title = 'AnimeAPI Admin'
admin.site.site_header = 'AnimeAPI Admin'


@admin.register(Genre, Studio)
class GenreStudioAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'title', 'created_at']
    list_display_links = ['id', 'slug']
    search_fields = ['title']
    list_filter = ['title', 'created_at']


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'title', 'score', 'type', 'season', 'studio', 'image', 'created_at']
    list_display_links = ['id', 'slug']
    search_fields = ['title']
    list_filter = ['title', 'score', 'studio', 'type', 'season', 'created_at']
