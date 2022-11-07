from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserCreateSerializer, UserSerializer
from main_app.serializers import AnimeListSerializer, AnimeDetailSerializer
from main_app.pagination import AnimePaginationClass
from main_app.models import Anime


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serialized_data = UserCreateSerializer(data=self.request.POST)
        response_data = {}
        if serialized_data.is_valid():
            user = serialized_data.save()
            response_data['response'] = True
            response_data['new_user'] = UserSerializer(user, many=False).data
            return Response(response_data, status=200)
        return Response(serialized_data.errors)


class FavoriteAnimeViewSet(ModelViewSet):
    serializer_class = AnimeListSerializer
    pagination_class = AnimePaginationClass
    http_method_names = ['get', 'delete']
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user
        return Anime.objects.select_related('studio', 'season').prefetch_related('genres', 'favorites')\
            .filter(favorites__user=user)

    def retrieve(self, request, *args, **kwargs):
        anime = self.get_queryset().get(slug=kwargs.get('slug'))
        serialized_anime = AnimeDetailSerializer(anime, many=False).data
        return Response({'anime': serialized_anime}, status=200)

    def destroy(self, request, *args, **kwargs):
        user_favorites = request.user.favorites.all()
        user_favorites.filter(anime__slug=kwargs.get('slug')).delete()
        return Response({'success': 'Anime has been deleted from favorites'}, status=200)
