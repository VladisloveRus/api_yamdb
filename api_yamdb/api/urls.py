from django.urls import include, path

from api.views import TitleViewSet, CategoryViewSet, GenreViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"genres", GenreViewSet, basename='genres')
router.register(r"categories", CategoryViewSet, basename='categories')
router.register(r"titles", TitleViewSet, basename='titles')


urlpatterns = [
    path("v1/", include(router.urls)),
]