from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, TemplateView

from apps.api.models import RiotSummoner
from apps.core.forms import ApiDisclaimerForm

from .forms import SummonerForm


class RegisterView(FormView):
    template_name = 'summoner/register.html'
    form_class = SummonerForm
    success_url = reverse_lazy('summoner.thanks')

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)


class ThanksView(TemplateView):
    template_name = 'summoner/thanks.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'summoner/profile.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(ProfileView, self).get_context_data(*args, **kwargs)

        context_data.update({
            'summoner': self.request.user,
        })

        return context_data


class UpdateSummonerNameView(LoginRequiredMixin, FormView):
    template_name = 'summoner/update_name.html'
    form_class = ApiDisclaimerForm
    success_url = reverse_lazy('summoner.profile')

    def form_valid(self, form):
        summoner = self.request.user

        riot_summoner = RiotSummoner.by_riot_id(
            summoner.riot_id,
            summoner.region
        )

        if not riot_summoner.name == summoner.summoner_name:
            summoner.summoner_name = riot_summoner.name
            summoner.save()

        return super(UpdateSummonerNameView, self).form_valid(form)
