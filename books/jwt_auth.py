from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

User = get_user_model()

ALGO = settings.JWT_AUTH.get("ALGORITHM", "HS256")
ACCESS_LIFETIME = int(settings.JWT_AUTH.get("ACCESS_TOKEN_LIFETIME", 300))
REFRESH_LIFETIME = int(settings.JWT_AUTH.get("REFRESH_TOKEN_LIFETIME", 10800))

def now_utc():
    return datetime.now(timezone.utc)

def _encode(payload: dict) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)

def make_access(user_id: int) -> str:
    iat = int(now_utc().timestamp())
    exp = int((now_utc() + timedelta(seconds=ACCESS_LIFETIME)).timestamp())
    payload = {"typ": "access", "sub": str(user_id), "iat": iat, "exp": exp}
    return _encode(payload)

def make_refresh(user_id: int, jti: str | None = None) -> str:
    iat = int(now_utc().timestamp())
    exp = int((now_utc() + timedelta(seconds=REFRESH_LIFETIME)).timestamp())
    payload = {"typ": "refresh", "sub": str(user_id), "iat": iat, "exp": exp}
    if jti:
        payload["jti"] = jti
    return _encode(payload)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGO])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Токен протерміновано")
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed("Некоректний токен")

class JWTAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        if len(auth) == 1:
            raise exceptions.AuthenticationFailed("Відсутній токен")
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed("Некоректний заголовок авторизації")

        token = auth[1].decode("utf-8")
        payload = decode_token(token)

        if payload.get("typ") != "access":
            raise exceptions.AuthenticationFailed("Очікувався access-токен")

        sub = payload.get("sub")
        if sub is None:
            raise exceptions.AuthenticationFailed("В токені відсутній sub")

        try:
            user = User.objects.get(pk=int(sub))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Користувача не існує")
        except (ValueError, TypeError):
            raise exceptions.AuthenticationFailed("Некоректний sub у токені")

        return (user, token)
