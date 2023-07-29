from django.db.models import Avg
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorModeratorAdminOrReadOnly
from api.serializers import (SignUpSerializer, TokenSerializer, UserSerializer,
                             CategorySerializer, GenreSerializer, CommentSerializer,
                             TitleSerializer, ReadOnlyTitleSerializer, ReviewSerializer)
from reviews.models import Category, Genre, Review, Title
from .mixins import ListCreateDestroyViewSet
from users.models import User


class APISignUp(APIView):
    """
    Регистрация пользователя.
    Получить код подтверждения на переданный email.
    Использовать имя 'me' в качестве username запрещено.
    """

    def post(self, request):
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('username') == 'me':
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Confirmation code',
            message=f'Hello, {(user.username)}! You have been sent'
                    f' a confirmation code! {(confirmation_code)}',
            from_email='from@example.com',
            recipient_list=[request.data['email']],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    """

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=request.data['username'])
        confirmation_code = request.data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Права доступа у администратора по urls /users/ и /users/username/:
        -Получение списка всех пользователей и добавления пользователя /users/.
        -Получение, изменение данных, удаление прользователя по username/.
    Права доступа у любого авторизованного пользователя в функции /users/me/:
        -Получение и изменение данных своей учётной записи.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, IsAuthenticated)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """
        Если метод запроса - GET, возвращает сериализованные данные
        о текущем пользователе.
        Если метод запроса - PATCH, обновляет информацию
        о текущем пользователе на основе предоставленных данных.
        """
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if serializer.validated_data.get('role'):
                serializer.validated_data.pop('role')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet for Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet for Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet for Title."""
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Получить список комментариев.
    Добавить новый комментарий к отзыву.
    Получить комментарий по id.
    Обновить комментарий по id.
    Удалить комментарий."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_review(self):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id'),)
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Получить список отзывов.
    Добавить новый отзыв.
    Получить отзыв по id.
    Обновить отзыв по id.
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
