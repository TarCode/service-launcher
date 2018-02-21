from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from django.views.generic import TemplateView

from . import views

import debug_toolbar

admin.autodiscover()

urlpatterns = (
    # Dashboard
		url(r'^$', TemplateView.as_view(template_name='home.html')),
		url(r'^wallet/', TemplateView.as_view(template_name='wallet.html')),
		url(r'^market/', TemplateView.as_view(template_name='market.html')),
    url(r'^dashboard/', include(admin.site.urls)),
    # Views
    url(r'^api/', include('launcher_service.urls', namespace='launcher_service')),
)

# Add debug URL routes
if settings.DEBUG:
    urlpatterns = (
        url(r'^$', views.index, name='index'),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ) + urlpatterns
