from django import forms

from apps.api.models import RiotSummoner
from apps.api.exceptions import APIError

from .models import Summoner


class SummonerForm(forms.ModelForm):
    summoner_name = forms.CharField(label='Summoner name', max_length=32)

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="""Enter the same password as above, for verification.
            I suggest you don't use your LoL password for safety reasons."""
    )

    riot_id = None

    class Meta:
        model = Summoner
        fields = ['email', 'region', 'summoner_name']

    # TODO: Check for duplicate usernames before calling the API

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The passwords do not match")

        return password2

    def clean_summoner_name(self):
        name = self.cleaned_data['summoner_name']
        region = self.cleaned_data['region']

        try:
            riot_summoner = RiotSummoner.by_summoner_name(name, region)
        except APIError as e:
            if e.status == 404:  # Not found
                # This also should keep out a lot of bot accounts
                raise forms.ValidationError("Summoner not found!")
            else:
                raise e

        self.riot_id = riot_summoner.id

        return name

    def save(self, commit=True):
        user = super(SummonerForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if self.riot_id is not None:  # Should always be True
            user.riot_id = self.riot_id

        if commit:
            user.save()

        return user
