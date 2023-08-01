from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from rest_framework import routers

from posts.views import PostsViewSet
from users.views.users import UsersViewSet
from users.views.auth import CustomAuthToken

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts/?', PostsViewSet, basename='posts')
router.register(r'users/?', UsersViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, 'apis'), namespace='apis')),
    path('token/', CustomAuthToken.as_view()),

    path('', RedirectView.as_view(pattern_name='users', permanent=False)),
]
