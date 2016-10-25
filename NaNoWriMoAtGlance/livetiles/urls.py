from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from views import *

urlpatterns = patterns('',
                       url('^glance', index),
                       url('^notification/(?P<type>\w+)/(?P<source>.*)', notification),
                       url('^$', TemplateView.as_view(template_name='livetiles/selector.html')),
                      )