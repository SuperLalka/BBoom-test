from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from posts.models import Post
from posts.serializers import PostSerializer
from users.forms import PostForm
from users.permissions import IsObjectOwnerPermission


class PostsViewSet(viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "destroy":
            self.permission_classes = [IsObjectOwnerPermission]
        return super().get_permissions()

    def create(self, request: Request, *args, **kwargs) -> Response:
        if "multipart/form-data" in request.headers.get("Content-Type"):
            form = PostForm(request.POST)
            if not form.is_valid():
                return Response(
                    form.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = form.cleaned_data
        else:
            data = request.data

        data = {
            **data,
            "user": self.request.user.id
        }

        instance = self.get_serializer(data=data)
        instance.is_valid(raise_exception=True)
        instance.save()
        return Response(instance.data, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, pk: int = None) -> Response:
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
