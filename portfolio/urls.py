from django.urls import path

from .views import erp, home

urlpatterns = [
    path("", home, name="home"),
    path("erp/", erp, name="erp"),
]
