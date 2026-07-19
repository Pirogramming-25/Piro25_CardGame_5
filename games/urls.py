from django.urls import path

from . import views


app_name = "games"

urlpatterns = [
    path("create/", views.game_create, name="create"),
    path("<int:pk>/", views.game_detail, name="detail"),
]
