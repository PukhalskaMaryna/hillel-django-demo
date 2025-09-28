from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from books import views as books_views
from django.views.generic import TemplateView

urlpatterns = [
    path('files/', books_views.files_list, name='files_list'),
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),  # ГОЛОВНА
    path("books/", include("books.urls")),                                   # КАТАЛОГ НА /books/
    path("api/", include("books.api")),                                       # API
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
