from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from books import views as books_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token  # додай імпорт

urlpatterns = [
    path('token/', books_views.token_page, name='token_page'),
    path('files/', books_views.files_list, name='files_list'),
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("books/", include("books.urls")),
    path("api/", include("books.api")),

    # зручно: POST {"username": "...", "password": "..."} -> {"token": "..."}
    path("api/token/", obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
