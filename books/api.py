from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated  # поруч з іншими імпортами

class HelloView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"hello": request.user.username})

router = DefaultRouter()
try:
    from .views import BookViewSet
    router.register(r'books', BookViewSet, basename='book')
except Exception:
    pass

from .jwt_auth import make_access, make_refresh, decode_token

class ObtainJWT(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Невірні облікові дані"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"access": make_access(user.id), "refresh": make_refresh(user.id)})

class RefreshJWT(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"detail": "Потрібен refresh токен"}, status=status.HTTP_400_BAD_REQUEST)
        payload = decode_token(refresh)
        if payload.get("typ") != "refresh":
            return Response({"detail": "Очікувався refresh-токен"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = int(payload["sub"])
        return Response({"access": make_access(user_id), "refresh": make_refresh(user_id)})

urlpatterns = [
    path('', include(router.urls)),
    path('token/', ObtainJWT.as_view(), name='api_token_obtain'),
    path('token/refresh/', RefreshJWT.as_view(), name='api_token_refresh'),
    path('hello/', HelloView.as_view(), name='hello'),
	
]
