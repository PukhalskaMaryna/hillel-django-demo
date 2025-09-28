# books/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    """
    Дозволяє будь-кому робити безпечні запити (GET/HEAD/OPTIONS).
    Небезпечні (POST/PUT/PATCH/DELETE) — тільки staff-користувачам.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_staff)
