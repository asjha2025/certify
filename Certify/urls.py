from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),  # روابط main مباشرة
    # path('certificates_app/', include("certificates_app.urls")),  # روابط certificates_app تبدأ بـ /certificates_app/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
