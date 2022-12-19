from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.db.models import Avg
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend

from api_yamdb.settings import CONSTANTS
from titles.models import Title, Genres, Categories
from users.models import CustomUser
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    GenresSerializer,
    CategoriesSerializer,
    TitlesSerializer,
    TitlesGetSerializer,
    SignUpSerializer,
    UserSerializer,
    MeSerializer,
    TokenSerializer
)
from .permission import (
    IsAuthorModeratorAdminOrReadOnly,
    IsAdminOrReadOnly,
    IsAdmin
)
from .filters import TitleFilters


class WithoutInstanceViewSet(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    pass


@api_view(['POST'])
def signup_user(request):
    """ Регистрация нового пользователя """

    user_serializer = SignUpSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        username = user_serializer.validated_data['username']
        email = user_serializer.validated_data['email']
        try:
            user, _ = CustomUser.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            return Response(
                f'{"Юзер уже создан"}', status=status.HTTP_400_BAD_REQUEST
            )

        user.confirmation_code = default_token_generator.make_token(user)
        user.save()

        send_mail(
            'Код подверждения', user.confirmation_code,
            [CONSTANTS['ADMIN_EMAIL']], (email,), fail_silently=False
        )
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    filterset_fields = 'username'
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'], detail=False,
        url_path='me', permission_classes=(IsAuthenticated,)
    )
    def get_patch_me(self, request):
        user = get_object_or_404(CustomUser, username=self.request.user)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )


@api_view(['POST'])
def get_access_token(request):
    """ Функция для выдачи токена юзеру """

    user_serializer = TokenSerializer(data=request.data)
    user_serializer.is_valid(raise_exception=True)

    username = user_serializer.validated_data['username']
    confirmation_code = user_serializer.validated_data['confirmation_code']

    current_user = get_object_or_404(CustomUser, username=username)

    if confirmation_code == current_user.confirmation_code:
        token = str(AccessToken.for_user(current_user))
        return Response(
            {"access_token": token}, status=status.HTTP_201_CREATED
        )

    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenresViewSet(WithoutInstanceViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')


class CategoriesViewSet(WithoutInstanceViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('title_review__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name',)
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesGetSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.title_review.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.title_review.get(id=self.kwargs.get('review_id'))
        except Exception:
            Exception('У данного произведения нет запрашиваемого отзыва.')
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        try:
            review = title.title_review.get(id=self.kwargs.get('review_id'))
        except Exception:
            Exception('У данного произведения нет запрашиваемого отзыва.')
        return review.comment_review.all()
