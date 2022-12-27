from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, GetToken,
                    ReviewViewSet, SignUp, TitleViewSet, UserProfile,
                    UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/users/me/', UserProfile.as_view(), name='profile'),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', GetToken.as_view(), name='gettoken'),
    path('v1/', include(router.urls)),
]
