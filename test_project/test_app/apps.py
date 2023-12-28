from django.apps import AppConfig


class TestAppConfig(AppConfig):
    # Tests and migrations run from different paths, automatically get the correct path
    split_name = __name__.split(".")
    name = ".".join(split_name[:-1])

    default_auto_field = "django.db.models.BigAutoField"
