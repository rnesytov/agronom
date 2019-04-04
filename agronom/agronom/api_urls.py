from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from rest_framework.documentation import include_docs_urls


"""
Root urlpatterns for all REST API.
"""

urlpatterns = [
    path('cadastral/', include('cadastral.api_urls')),
    path('cadastral/', include('fields.api_urls')),
    path('weather/', include('weather.api_urls')),
    path('ndvi/', include('ndvi.api_urls')),
]

if 'silk' in settings.INSTALLED_APPS and settings.ENABLE_UNSAFE_PROFILING:
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk')),
    ]

if settings.DEBUG:
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import permissions, authentication

    schema_view_yasg = get_schema_view(
        openapi.Info(
            title="Agronom API",
            default_version='v1',
            description="Test description",
            # terms_of_service="https://example.com/",
            contact=openapi.Contact(email="contact@agronom.twdev.ru"),
            license=openapi.License(name="Proprietary License"),
        ),
        # validators=['flex', 'ssv'],
        public=False,
        authentication_classes=(authentication.BasicAuthentication,),
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        path('docs/', include_docs_urls(title='Agronom API', permission_classes=(permissions.AllowAny,))),
        path('drfdocs/', include('rest_framework_docs.urls')),
        # Swagger-based autodoc
        url(
            r'^swagger(?P<format>\.json|\.yaml)$', schema_view_yasg.without_ui(cache_timeout=None),
            name='schema-json'
        ),
        path('swagger/', schema_view_yasg.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
        path('redoc/', schema_view_yasg.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    ]
