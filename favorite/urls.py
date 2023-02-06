# file: favorite/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.favorite_view),
    url(r'^edit/(\d+)$', views.edit_view),
    url(r'^add/(\d+)$', views.add_view),
    url(r'^del/(\d+)$', views.del_view),
]
