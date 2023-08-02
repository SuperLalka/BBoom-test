from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from bboom_test.settings import AUTHENTICATION_COOKIE_NAME
from posts.models import Post
from posts.serializers import PostSerializer
from users.forms import PostForm
from users.models import User
from users.serializers.users import UserSerializer


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request: Request) -> Response:
        if request.headers.get("Accept") == "application/json":
            return super().list(request)

        return render(request, 'users_list.html', context={
                'user_list': self.queryset
            }
        )

    def retrieve(self, request: Request, pk=None) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['GET'], detail=True)
    def user_posts(self, request: Request, pk: int) -> Response:
        queryset = Post.objects.filter(user_id=pk)
        response_data = PostSerializer(queryset, many=True).data

        if request.headers.get("Accept") == "application/json":
            return Response(response_data, status=status.HTTP_200_OK)

        return render(request, 'user_posts_list.html', context={
                'user_posts': response_data
            }
        )

    @action(methods=['GET'], detail=False)
    def user_cabinet(self, request: Request) -> Response:
        add_post_form = PostForm(request.POST)
        return render(request, 'user_cabinet.html', context={
                'add_post_form': add_post_form,
                'user_token': request.COOKIES.get(AUTHENTICATION_COOKIE_NAME)
            }
        )
