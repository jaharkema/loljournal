from django import forms


class ApiDisclaimerForm(forms.Form):
    agree = forms.BooleanField(
        label='I understand that I am making multiple calls to the Riot API and keep the request limit in mind.'
    )
