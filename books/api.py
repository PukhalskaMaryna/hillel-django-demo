from rest_framework import routers, viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("-id")
    serializer_class = BookSerializer

router = routers.DefaultRouter()
router.register(r"books", BookViewSet, basename="book")

urlpatterns = router.urls
