from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    path('cart/', include('cart.urls',namespace='mainapp')),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
