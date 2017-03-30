from django.conf.urls import url

from .views import FaqView

urlpatterns = [
    url(r'^$', FaqView.as_view(), name='faq.index'),
]
