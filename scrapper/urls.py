from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url='/admin/')),
    path('admin/', admin.site.urls),
    path('', include(("catalog.urls", "catalog")))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
