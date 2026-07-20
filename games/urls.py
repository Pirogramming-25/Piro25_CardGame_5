from django.urls import path

from . import views


app_name = "games"

urlpatterns = [
    path("create/", views.game_create, name="create"),
    path("history/", views.game_history, name="history"),
    path("<int:pk>/", views.game_detail, name="detail"),
    path("<int:pk>/counter/", views.game_counter, name="counter"),
    path("<int:pk>/cancel/", views.game_cancel, name="cancel"),
]


