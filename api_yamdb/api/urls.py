from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ReviewViewSet,
    CommentViewSet,
    TitlesViewSet,
    GenresViewSet,
    CategoriesViewSet,
    UserViewSet,
    signup_user,
    get_access_token
)


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('genres', GenresViewSet)
v1_router.register('categories', CategoriesViewSet)
v1_router.register('titles', TitlesViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('signup/', signup_user),
    path('token/', get_access_token, name="access_token_url"),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(v1_router.urls)),
]
