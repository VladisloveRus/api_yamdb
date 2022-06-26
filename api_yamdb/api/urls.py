from django.urls import include, path
from rest_framework import routers

from .views import (TitleViewSet,
                    CategoryViewSet,
                    GenreViewSet,
                    SignupViewSet,
                    create_jwt_token
                    )

router = routers.DefaultRouter()
router.register(r"genres", GenreViewSet, basename='genres')
router.register(r"categories", CategoryViewSet, basename='categories')
router.register(r"titles", TitleViewSet, basename='titles')


urlpatterns = [
    path("v1/auth/signup/", SignupViewSet.as_view()),
    path("v1/auth/token/", create_jwt_token),
    path("v1/", include(router.urls)),
]
