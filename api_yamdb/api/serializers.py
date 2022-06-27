from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError

from reviews.models import Category, CustomUser, Genre, Title


class UserSerializer(serializers.ModelSerializer):
    # current_user = serializers.SerializerMethodField("_user")

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
            # "current_user"
        )

    validators = [
        UniqueTogetherValidator(
            queryset=CustomUser.objects.all(),
            fields=["username", "email"]
        )
    ]

    def create(self, validated_data):
        confirmation_code = get_random_string(length=32)  # generate code
        username = validated_data["username"]
        if username == "me":
            raise ValidationError(code=400)
        email = str(validated_data["email"])
        user = CustomUser(
            username=username,
            email=email,
            confirmation_code=confirmation_code
        )
        current_user_admin = False
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            current_user_admin = request.user.is_admin
        if not current_user_admin:
            send_mail(
                "Код подтверждения для регистрации YamDB",
                f"{username} Ваш код подтверждения: {confirmation_code}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=(email,),
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
