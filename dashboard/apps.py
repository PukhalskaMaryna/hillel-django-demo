from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"

    def ready(self):
        # Імпортуємо ресівери при старті app (правильний відносний імпорт)
        from . import receivers  # noqa: F401
