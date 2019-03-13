from django.urls import path

from . import views

urlpatterns = [
    path('<int:cadastral_id>/fields/', views.FieldsView.as_view(), name='api_fields'),
]
