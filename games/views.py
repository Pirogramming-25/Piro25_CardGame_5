import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import GameCounterForm, GameCreateForm
from .models import Game


CARD_OPTIONS_SESSION_KEY = "game_card_options"


def _counter_card_options_session_key(pk):
    return f"game_counter_card_options_{pk}"


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


@login_required
def game_counter(request, pk):
    game = get_object_or_404(
        Game.objects.filter(defender=request.user, defender_card__isnull=True),
        pk=pk,
    )

    session_key = _counter_card_options_session_key(pk)
    if request.method == "GET":
        card_options = random.sample(range(1, 11), 5)
        request.session[session_key] = card_options
    else:
        card_options = request.session.get(session_key, [])

    form = GameCounterForm(
        request.POST or None,
        card_options=card_options,
    )

    if request.method == "POST" and form.is_valid():
        game.defender_card = form.cleaned_data["defender_card"]
        game.winning_rule = random.choice(Game.WinningRule.values)
        game.completed_at = timezone.now()

        if game.attacker_card != game.defender_card:
            attacker_wins = (
                game.attacker_card > game.defender_card
                if game.winning_rule == Game.WinningRule.HIGH
                else game.attacker_card < game.defender_card
            )
            game.winner = game.attacker if attacker_wins else game.defender

            loser = game.defender if attacker_wins else game.attacker
            loser_card = game.defender_card if attacker_wins else game.attacker_card
            winner_card = game.attacker_card if attacker_wins else game.defender_card

            game.winner.score += winner_card
            loser.score -= loser_card
            game.winner.save(update_fields=["score"])
            loser.save(update_fields=["score"])

        game.save()
        request.session.pop(session_key, None)
        return redirect("games:detail", pk=game.pk)

    return render(
        request,
        "games/game_counter.html",
        {"form": form, "game": game},
    )


@login_required
@require_POST
def game_cancel(request, pk):
    game = get_object_or_404(
        Game.objects.filter(attacker=request.user, defender_card__isnull=True),
        pk=pk,
    )
    game.delete()
    return redirect("games:history")
