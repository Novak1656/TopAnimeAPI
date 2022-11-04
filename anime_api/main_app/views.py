from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Anime, Genre, Studio
from .serializers import AnimeListSerializer, GenreSerializer, StudioSerializer, AnimeDetailSerializer
from .pagination import AnimePaginationClass, GenrePaginationClass, StudioPaginationClass
from rest_framework.permissions import AllowAny, IsAuthenticated
from users_app.models import UserAnimeFavorite

# Search Anime, Anime by seasons


class AnimeViewSet(ModelViewSet):
    queryset = Anime.objects.all().select_related('studio').prefetch_related('genres')
    serializer_class = AnimeListSerializer
    pagination_class = AnimePaginationClass
    permission_classes_by_action = {'list': [AllowAny], 'retrieve': [AllowAny]}
    http_method_names = ['get', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        anime_slug = kwargs.get('slug')
        anime_obj = self.get_queryset().get(slug=anime_slug)
        return Response({'anime': AnimeDetailSerializer(anime_obj, many=False).data})

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def add_in_favorite(self, request, slug):
        user = request.user
        anime = self.get_queryset().get(slug=slug)
        favorite, is_created = UserAnimeFavorite.objects.get_or_create(user=user, anime=anime)
        if not is_created:
            return Response({'error': f"The anime '{anime.title}' is already in your favorites"})
        return Response({'success': f"Anime '{anime.title}' added to favorites"}, status=200)


class GenresViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = GenrePaginationClass
    permission_classes = (AllowAny,)
    http_method_names = ['get', ]
    lookup_field = 'slug'

    @action(methods=['GET'], detail=True)
    def anime(self, request, slug):
        anime_by_genre = Genre.objects.get(slug=slug).anime.all().prefetch_related('genres').select_related('studio')
        if not anime_by_genre.exists():
            return Response({'anime': "There is not a single anime in this genre"})
        context = {'anime_count': anime_by_genre.count(), 'anime': AnimeListSerializer(anime_by_genre, many=True).data}
        return Response(context)


class StudiosViewSet(ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    pagination_class = StudioPaginationClass
    permission_classes = (AllowAny,)
    http_method_names = ['get', ]
    lookup_field = 'slug'

    @action(methods=['GET'], detail=True)
    def anime(self, request, slug):
        anime_by_studio = Anime.objects.prefetch_related('genres').select_related('studio').filter(studio__slug=slug)
        if not anime_by_studio.exists():
            return Response({'anime': "Don't any anime from this studio"})
        context = {'anime_count': anime_by_studio.count(),'anime': AnimeListSerializer(anime_by_studio, many=True).data}
        return Response(context)
