from django.urls import path

from . import views

urlpatterns = [
    path('', views.CadastralListCreateView.as_view(), name='api_cadastral'),
    path('<int:cadastral_id>/', views.CadastralRetrieveView.as_view(), name='api_cadastral'),
]
