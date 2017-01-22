from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='blog_index'),
    url(r'^(?P<year>\d{4})/(?P<slug>[\w\-_]+)$', views.post, name='blog_post'),
    url(r'^preview/(?P<slug>[\w\-_]+)$', views.post, {'allow_unpublished': True}, name='blog_preview'),
]
