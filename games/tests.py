from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Game


class GameCreateTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.attacker = User.objects.create_user(username="attacker")
        self.defender = User.objects.create_user(username="defender")
        self.client.force_login(self.attacker)

    def test_create_page_offers_five_unique_cards_between_one_and_ten(self):
        response = self.client.get(reverse("games:create"))

        choices = [
            value
            for value, _ in response.context["form"].fields[
                "attacker_card"
            ].choices
        ]
        self.assertEqual(len(choices), 5)
        self.assertEqual(len(set(choices)), 5)
        self.assertTrue(all(1 <= card <= 10 for card in choices))

    def test_create_page_excludes_attacker_from_opponents(self):
        response = self.client.get(reverse("games:create"))

        opponents = response.context["form"].fields["defender"].queryset
        self.assertNotIn(self.attacker, opponents)
        self.assertIn(self.defender, opponents)

    def test_game_is_created_with_offered_card(self):
        self.client.get(reverse("games:create"))
        card = self.client.session["game_card_options"][0]

        response = self.client.post(
            reverse("games:create"),
            {
                "defender": self.defender.pk,
                "attacker_card": card,
            },
        )

        game = Game.objects.get()
        self.assertRedirects(response, reverse("games:detail", args=[game.pk]))
        self.assertEqual(game.attacker, self.attacker)
        self.assertEqual(game.defender, self.defender)
        self.assertEqual(game.attacker_card, card)

    def test_card_not_offered_by_server_is_rejected(self):
        session = self.client.session
        session["game_card_options"] = [1, 2, 3, 4, 5]
        session.save()

        response = self.client.post(
            reverse("games:create"),
            {
                "defender": self.defender.pk,
                "attacker_card": 10,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Game.objects.exists())

    def test_login_is_required(self):
        self.client.logout()

        response = self.client.get(reverse("games:create"))

        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('games:create')}",
        )
