from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^images/(?P<path>.*)$', 'django.views.static.serve'),
                       url(r'^', include('apps.task.urls', namespace="task")),
                       url('^', include('django.contrib.auth.urls')),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)