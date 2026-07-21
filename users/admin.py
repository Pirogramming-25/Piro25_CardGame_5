from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("게임 정보", {"fields": ("score",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("게임 정보", {"fields": ("score",)}),
    )
