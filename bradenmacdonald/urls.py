from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static
from django.views.generic.base import RedirectView

from bradenmacdonald import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^blog$', RedirectView.as_view(url='/blog/')),
    url(r'^blog/', include('blog.urls')),
    url(r'^quotes$', RedirectView.as_view(url='/quotes/')),
    url(r'^quotes/', include('bradenmacdonald.quotes.urls')),
    url(r'^backend/', include(admin.site.urls)),
    url(r'^', include('bradenmacdonald.content.urls')),
]

if settings.SERVE_MEDIA_FILES:
    # On development servers, we need to manually specify that the media files
    # should be served:
    prefix = settings.MEDIA_URL.strip('/') + '/'
    urlpatterns += [
        url(prefix + r'(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT, }),
    ]
