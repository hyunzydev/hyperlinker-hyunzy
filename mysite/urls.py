from django.apps import apps
from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("weblinks/", include("weblinks.urls")),
    path("", home, name="home"),
    path("", include("core.urls")),
]


if apps.is_installed("debug_toolbar"):
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
