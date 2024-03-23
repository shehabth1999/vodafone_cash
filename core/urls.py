from django.conf import settings
from django.contrib import admin
from django.urls import path, include,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import debug_toolbar

admin.site.site_header = 'Maloma'
admin.site.site_title = 'Maloma'

from institution.urls import urlpatterns as Institution


schema_view = get_schema_view(
    openapi.Info(
        title               = admin.site.site_header,
        default_version     = 'v1',
        # description         = "Test description",
        # terms_of_service    = f"{settings.ALLOWED_HOSTS[0]}terms/",
        # contact             = openapi.Contact(email="dev.mohamed.arfa@gmail.com"),
        # license             = openapi.License(name="Test License"),
    ),
    public                  =True,
    permission_classes      =(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('jet/', include('jet.urls', 'jet')),                               # Django JET URLS

    path('auth/',           include('authentication.urls'), name = 'auth'),
    path('social_auth/',    include('social_auth.urls'),    name="social_auth"),
    path('institution/',    include('institution.urls'),    name="institution"),
]


if settings.DEBUG: 
    urlpatterns +=[
        # Toolbar
        path('__debug__/', include(debug_toolbar.urls)),
        # Swagger
        path('swagger', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
    ]
