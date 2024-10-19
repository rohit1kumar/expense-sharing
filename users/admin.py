from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "mobile_number", "created_at", "updated_at")
    search_fields = ("email", "name", "mobile_number")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(User, UserAdmin)
