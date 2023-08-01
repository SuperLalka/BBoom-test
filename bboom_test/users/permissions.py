from rest_framework.permissions import IsAuthenticated

from posts.models import Post


class IsObjectOwnerPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        model_object = view.get_object()
        if isinstance(model_object, Post):
            return model_object.user_id == request.user.id
