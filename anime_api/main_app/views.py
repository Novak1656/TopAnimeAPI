from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Anime, Genre, Studio, Season
from .serializers import AnimeListSerializer, GenreSerializer, StudioSerializer, AnimeDetailSerializer, SeasonSerializer
from .pagination import AnimePaginationClass, GenrePaginationClass, StudioPaginationClass, SeasonPaginationClass
from rest_framework.permissions import AllowAny, IsAuthenticated
from users_app.models import UserAnimeFavorite


class AnimeViewSet(ModelViewSet):
    queryset = Anime.objects.all().select_related('studio', 'season').prefetch_related('genres')
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

    @action(methods=['GET'], detail=False)
    def search(self, request):
        search_word = request.GET.get('search_word')
        search_results = Anime.objects.filter(title__icontains=search_word)\
            .select_related('studio', 'season').prefetch_related('genres')
        if search_results.exists():
            serialized_results = AnimeListSerializer(search_results, many=True).data
            context = {
                'search_word': search_word,
                'anime_count': search_results.count(),
                'search_results': serialized_results
            }
            return Response(context, status=200)
        return Response({'search_word': search_word, 'search_results': 'Nothing was found for your query'}, status=200)


class GenresViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = GenrePaginationClass
    permission_classes = (AllowAny,)
    http_method_names = ['get', ]
    lookup_field = 'slug'

    @action(methods=['GET'], detail=True)
    def anime(self, request, slug):
        anime_by_genre = Genre.objects.get(slug=slug).anime.all().prefetch_related('genres')\
            .select_related('studio', 'season')
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
        anime_by_studio = Anime.objects.prefetch_related('genres').select_related('studio', 'season')\
            .filter(studio__slug=slug)
        if not anime_by_studio.exists():
            return Response({'anime': "Don't any anime from this studio"})
        context = {'anime_count': anime_by_studio.count(),'anime': AnimeListSerializer(anime_by_studio, many=True).data}
        return Response(context)


class SeasonViewSet(ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    pagination_class = SeasonPaginationClass
    permission_classes = [AllowAny, ]
    http_method_names = ['get', ]
    lookup_field = 'slug'

    @action(methods=['GET'], detail=True)
    def anime(self, request, slug):
        anime_by_seasons = Anime.objects.filter(season__slug=slug).prefetch_related('genres')\
            .select_related('studio', 'season')
        if not anime_by_seasons.exists():
            return Response({'anime': "Don't any anime from this season"})
        serialized_anime = AnimeListSerializer(anime_by_seasons, many=True).data
        return Response({'anime_count': anime_by_seasons.count(), 'anime': serialized_anime}, status=200)
