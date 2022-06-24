from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.utils.crypto import get_random_string

from reviews.models import Category, CustomUser, Genre, Title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )

    validators = [
        UniqueTogetherValidator(
            queryset=CustomUser.objects.all(),
            fields=["username", "email"]
        )
    ]

    def create(self, validated_data):
        confirmation_code = get_random_string(length=32)  # generate code
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data["email"],
            confirmation_code=confirmation_code
        )
        user.save()
        return validated_data


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для GET."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )
        # read_only_fields = ("id",)


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для POST, PATH."""
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )
