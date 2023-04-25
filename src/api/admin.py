from django.contrib import admin

from .models import DailySolution


@admin.register(DailySolution)
class DailySolutionAdmin(admin.ModelAdmin):
    list_display = ("date", "solution", "created_at", "updated_at")
