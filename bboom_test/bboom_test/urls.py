from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions, routers

from posts.views import PostsViewSet
from users.views.users import UsersViewSet
from users.views.auth import CustomAuthToken

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet, basename='posts')
router.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, 'apis'), namespace='apis')),
    path('token/', CustomAuthToken.as_view(), name='token'),

    path('', RedirectView.as_view(pattern_name='users', permanent=False)),
]


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

redoc_urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += redoc_urlpatterns
