from django.urls import path

from . import views

urlpatterns = [
    path('', views.NDVIView.as_view(), name='api_ndvi'),
]
