from django.core.mail import EmailMessage
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .mixins import (CreateDestroyListViewSet,
                     CreateDestroyUpdateDeleteListViewSet)
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializers,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializers, SignUpSerializer,
                          TitleCrudSerializer, TitleGetSerializer,
                          UserSerializer, ProfilePatchSerializer)
from reviews.models import Category, Comment, Genre, Review, Title, User


class TitleViewSet(CreateDestroyUpdateDeleteListViewSet):
    queryset = (
        Title.objects.annotate(rating=Avg('reviews__score')).all()
        .order_by('-rating')
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'delete', 'patch')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitleCrudSerializer


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class UserViewSet(CreateDestroyUpdateDeleteListViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = ('username')


class ReviewViewSet(CreateDestroyUpdateDeleteListViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(CreateDestroyUpdateDeleteListViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class SignUp(views.APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'проверочный код {user.confirmation_code}'
        )
        data = {
            'email_subject': 'Код подтверждения',
            'email_body': email_body,
            'to': user.email
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetToken(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if not User.objects.filter(username=data.get('username')).exists():
            return Response(
                {'username': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        user = User.objects.get(username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неправильный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProfile(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_obj(self, id):
        return User.objects.get(pk=id)

    def get(self, request):
        user = self.get_obj(request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = self.get_obj(request.user.id)
        serializer = ProfilePatchSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
