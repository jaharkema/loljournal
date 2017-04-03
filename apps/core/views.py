from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView, View


class HomeView(TemplateView):
    template_name = 'core/home.html'


class RiotTextView(View):
	def get(*args, **kwargs):
		content = settings.RIOT_VERIFICATION_TEXT
		return HttpResponse(content, content_type='text/plain; charset=utf8')
