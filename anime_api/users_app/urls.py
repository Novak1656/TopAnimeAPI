from django.urls import path, include
from .views import UserCreateAPIView, FavoriteAnimeViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'favorites', FavoriteAnimeViewSet, basename='favorites')

urlpatterns = [
    path('api-auth', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('registration/', UserCreateAPIView.as_view(), name='registration'),
    path('', include(router.urls))
]
