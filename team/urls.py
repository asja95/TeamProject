from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name='door.html'), name='home'),
    path('admin/', admin.site.urls),
    url('first/', TemplateView.as_view(template_name='first.html'), name='home1'),
    url('second/', TemplateView.as_view(template_name='second.html'), name='home2'),
    url('third/', include('interest.urls')),
    path('analy/', include('analy.urls')),
    path('search/', include('search.urls')),
    path('interest/', include('interest.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)