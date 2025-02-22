from django.contrib import admin
from .models import WebLink


class WebLinkAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(WebLink, WebLinkAdmin)
