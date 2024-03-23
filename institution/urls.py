from django.urls import include,path

urlpatterns = [
    path('api/', include(f'{__package__}.api.urls')),
]