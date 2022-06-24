from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, CustomUser, Genre, Title
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    UserSerializer
)
from .mixins import ListCreateDestroyViewSet
from .tokens import get_jwt_token


class SignupViewSet(CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, partial=False)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_jwt_token(request):
    user = get_object_or_404(
        CustomUser,
        username=request.data['username'],
    )
    if user.confirmation_code != request.data.get('confirmation_code'):
        raise ValidationError(code=400)
    return Response(get_jwt_token(user), status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitleSerializer
