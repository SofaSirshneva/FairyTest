from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from FairyTail1 import settings
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('tests.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = Error404Page.as_view()
