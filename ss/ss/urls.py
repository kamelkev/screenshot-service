from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from ss import views

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^screenshot$', views.screenshot),
)
