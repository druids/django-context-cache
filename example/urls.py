from django.urls import path

from apps.app import views


urlpatterns = [
    path('', views.test_view),
]
