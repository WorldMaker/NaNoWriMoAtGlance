from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url('^glance', views.index),
    url('^notification/(?P<type>\w+)/(?P<source>.*)', views.notification),
    url('^$', TemplateView.as_view(template_name='livetiles/selector.html')),
]