from django.contrib import admin

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "attacker",
        "defender",
        "attacker_card",
        "defender_card",
        "created_at",
    )
    list_filter = ("winning_rule", "created_at")
    search_fields = ("attacker__username", "defender__username")
