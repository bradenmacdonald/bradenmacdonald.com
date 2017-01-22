from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^projects/?$', views.projects),
    url(r'^(?P<path>[\w\-_\/]+)$', views.page),
]
