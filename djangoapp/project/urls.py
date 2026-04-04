# Main URL file - this is the first place Django looks when
# a request comes in, and it decides where to send it.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # All blog-related URLs are handled in blog/urls.py
    path('', include('blog.urls')),

    # Needed for the Summernote editor to handle image uploads
    path('summernote/', include('django_summernote.urls')),

    # Django's built-in admin panel
    path('admin/', admin.site.urls),
]

# In development, Django serves uploaded images directly.
# In production a proper web server like nginx handles this instead.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
