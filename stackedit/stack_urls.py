from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^viewer$', views.viewer),
    url(r'^recovery$', views.recovery),
]