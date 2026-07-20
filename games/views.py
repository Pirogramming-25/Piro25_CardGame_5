import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GameCreateForm
from .models import Game


CARD_OPTIONS_SESSION_KEY = "game_card_options"


@login_required
def game_create(request):
    if request.method == "GET":
        card_options = random.sample(range(1, 11), 5)
        request.session[CARD_OPTIONS_SESSION_KEY] = card_options
    else:
        card_options = request.session.get(CARD_OPTIONS_SESSION_KEY, [])

    form = GameCreateForm(
        request.POST or None,
        attacker=request.user,
        card_options=card_options,
    )

    if request.method == "POST" and form.is_valid():
        game = form.save(commit=False)
        game.attacker = request.user
        game.save()
        request.session.pop(CARD_OPTIONS_SESSION_KEY, None)
        return redirect("games:detail", pk=game.pk)

    return render(
        request,
        "games/game_create.html",
        {"form": form},
    )


@login_required
def game_history(request):
    games = Game.objects.filter(
        Q(attacker=request.user) | Q(defender=request.user),
    ).select_related("attacker", "defender", "winner")

    return render(request, "games/game_history.html", {"games": games})


@login_required
def game_detail(request, pk):
    game = get_object_or_404(
        Game.objects.filter(
            Q(attacker=request.user) | Q(defender=request.user),
        ),
        pk=pk,
    )
    return render(request, "games/game_detail.html", {"game": game})
