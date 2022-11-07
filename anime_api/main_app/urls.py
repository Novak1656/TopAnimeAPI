from django.urls import path, include
from .views import AnimeViewSet, GenresViewSet, StudiosViewSet, SeasonViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'studios', StudiosViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'', AnimeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
