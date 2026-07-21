from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q


class Game(models.Model):
    class WinningRule(models.TextChoices):
        HIGH = "HIGH", "높은 숫자 승리"
        LOW = "LOW", "낮은 숫자 승리"

    attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attacks",
    )
    defender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="defenses",
    )
    attacker_card = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    defender_card = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True,
    )
    winning_rule = models.CharField(
        max_length=4,
        choices=WinningRule.choices,
        blank=True,
    )
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="wins",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=~Q(attacker=F("defender")),
                name="game_attacker_and_defender_differ",
            ),
        ]

    @property
    def is_completed(self):
        return self.defender_card is not None

    def __str__(self):
        return f"{self.attacker} vs {self.defender}"
