from django.conf.urls import url

from .views import RegisterView, ThanksView, ProfileView, UpdateSummonerNameView


urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='summoner.register'),
    url(r'^thanks/$', ThanksView.as_view(), name='summoner.thanks'),
    url(r'^profile/$', ProfileView.as_view(), name='summoner.profile'),
    url(r'^update_name/$', UpdateSummonerNameView.as_view(), name='summoner.update_name'),
]
