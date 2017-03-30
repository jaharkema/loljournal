from django.views.generic.list import ListView

from .models import Question


class FaqView(ListView):
    model = Question
    template_name = 'faq/faq.html'
    context_object_name = 'questions'
