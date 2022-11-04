from rest_framework import serializers
from .models import Anime, Genre, Studio


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['created_at']


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        exclude = ['created_at']


class AnimeListSerializer(serializers.ModelSerializer):
    studio = StudioSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Anime
        exclude = ['description', 'created_at']
        depth = 1


class AnimeDetailSerializer(serializers.ModelSerializer):
    studio = StudioSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Anime
        fields = '__all__'
        depth = 1
