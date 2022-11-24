from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', include('blog_post_app.urls')),
    path('user/', include('user.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
