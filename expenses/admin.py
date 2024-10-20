from django.contrib import admin
from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "total_amount",
        "paid_by",
        "created_at",
    )
    search_fields = ("title", "paid_by")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Expense, ExpenseAdmin)
