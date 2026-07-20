from django import forms

from users.models import User

from .models import Game


class GameCreateForm(forms.ModelForm):
    attacker_card = forms.TypedChoiceField(
        label="카드",
        coerce=int,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Game
        fields = ("defender", "attacker_card")
        labels = {"defender": "공격 대상"}

    def __init__(self, *args, attacker, card_options, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["defender"].queryset = User.objects.exclude(pk=attacker.pk)
        self.fields["attacker_card"].choices = [
            (card, str(card)) for card in card_options
        ]


class GameCounterForm(forms.ModelForm):
    defender_card = forms.TypedChoiceField(
        label="카드",
        coerce=int,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Game
        fields = ("defender_card",)

    def __init__(self, *args, card_options, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["defender_card"].choices = [
            (card, str(card)) for card in card_options
        ]
