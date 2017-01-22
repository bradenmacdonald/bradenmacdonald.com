from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='quotes_index'),
    url(r'^by\-(?P<author_id>\d+)$', views.author, name='quotes_author'),
]
