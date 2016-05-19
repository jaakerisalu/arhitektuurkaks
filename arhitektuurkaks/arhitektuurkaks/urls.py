from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

from arhitektuurkaks import views
from arhitektuurkaks.views import TvSeriesView, TvSeriesDetailView, TvSeriesEditView

admin.autodiscover()

urlpatterns = [
    url(r'', include('accounts.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^s/$', TvSeriesView.as_view(), name='series'),
    url(r'^s/(?P<series_id>\d+)/$', TvSeriesDetailView.as_view(), name='series-detail'),
    url(r'^s/(?P<series_id>\d+)/edit/$', TvSeriesEditView.as_view(), name='series-edit'),
    url(r'^api/', views.get_object, name='series-api'),
    url(r'^s/api/', views.get_object, name='series-api'),

    url(r'^tagauks/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if not settings.DEBUG:
    handler500 = 'arhitektuurkaks.views.server_error'
    handler404 = 'arhitektuurkaks.views.page_not_found'
