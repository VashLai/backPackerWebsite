# file: index/urls.py

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index_view)
]