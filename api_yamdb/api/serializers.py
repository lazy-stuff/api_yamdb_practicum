from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import Review, Comment
from titles.models import Title, Genres, Categories
from users.models import CustomUser


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genres."""

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Categories."""

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitlesGetSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели Titles."""
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для изменений модели Titles."""
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title,
                                     author=request.user).exists():
                raise serializers.ValidationError(
                    'Нельзя добваить более одного отзыва на произведение'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150, required=True)
    username = serializers.CharField(max_length=50, required=True)

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError('Нельзя использовать логин me')
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Это имя пользователя уже занято.'
            )
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Этот email уже зарегистрирован.'
            )
        return data

    class Meta:
        fields = ('username', 'email')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )


class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
