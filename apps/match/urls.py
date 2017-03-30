from django.conf.urls import url

from .views import MatchListView, RetrieveRecentView, MatchUpdateView

urlpatterns = [
    url(r'^retrieve/$', RetrieveRecentView.as_view(), name='match.retrieve'),
    url(r'^list/$', MatchListView.as_view(), name='match.list'),
    url(r'^(?P<pk>[0-9]+)/$', MatchUpdateView.as_view(), name='match.update'),
]
