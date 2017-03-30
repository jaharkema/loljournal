from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from apps.api.models import RiotGame, RiotChampion
from apps.core.forms import ApiDisclaimerForm

from .models import Match


class RetrieveRecentView(LoginRequiredMixin, FormView):
    template_name = 'match/retrieve.html'
    form_class = ApiDisclaimerForm
    success_url = reverse_lazy('match.list')

    def form_valid(self, form):
        summoner = self.request.user
        recent_matches = RiotGame.recent_for_summoner(
            summoner.riot_id,
            summoner.region
        )

        champions = {}

        for match in recent_matches:
            if match.champion_id not in champions:

                riot_champ = RiotChampion.by_id(
                    match.champion_id,
                    summoner.region
                )

                champions.update({
                    riot_champ.id: riot_champ,
                })

            riot_champion = champions[match.champion_id]

            Match.objects.get_or_create(
                riot_id=match.id,
                summoner=summoner,
                defaults={
                    'win': match.win,
                    'champion_id': riot_champion.id,
                    'champion_name': riot_champion.name,
                    'created': match.created,
                    'kills': match.kills,
                    'deaths': match.deaths,
                    'assists': match.assists,
                    'minions': match.minions_killed,
                    'game_type': match.game_type,
                }
            )

        return super(RetrieveRecentView, self).form_valid(form)


class MatchListView(LoginRequiredMixin, ListView):
    model = Match
    template_name = 'match/list.html'
    context_object_name = 'matches'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = self.model.objects.filter(summoner=self.request.user)

        game_type = self.request.GET.get('game_type', None)

        if game_type:
            queryset = queryset.filter(game_type=game_type)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super(MatchListView, self).get_context_data(
            *args, **kwargs
        )

        game_type = self.request.GET.get('game_type', None)
        matches = Match.objects.all().order_by('game_type')
        game_types = matches.values_list('game_type', flat=True).distinct()

        context_data.update({
            'game_types': game_types,
            'selected_game_type': game_type,
        })

        return context_data


class MatchUpdateView(LoginRequiredMixin, UpdateView):
    model = Match
    template_name = 'match/update.html'
    fields = ['notes']
    success_url = reverse_lazy('match.list')
